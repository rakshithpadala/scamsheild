"""Model Training and Comparison for ScamShield AI.

Trains and compares:
1. Six binary text classifiers on UCI SMS Spam Collection:
   - Logistic Regression
   - K-Nearest Neighbors (KNN)
   - Decision Tree
   - Random Forest
   - Support Vector Machine (Linear SVM)
   - XGBoost
   Evaluates: Accuracy, Precision, Recall, F1, ROC-AUC, FPR, FNR, Train Time.
   Selects best model prioritizing Recall at acceptable FPR (FPR <= 0.05).

2. Multi-class Category Classifiers on Synthetic Scams (10 categories):
   - TF-IDF + Logistic Regression
   - SentenceTransformer (all-MiniLM-L6-v2) + Logistic Regression
   Evaluated against the handwritten test benchmark (40 scam rows across 10 categories).

Logs all runs to MLflow and outputs summary to docs/EVAL.md.
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("train_text_models")

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ML_DATA_DIR = ROOT_DIR / "ml" / "data"
ARTIFACTS_DIR = ROOT_DIR / "ml" / "artifacts"
DOCS_DIR = ROOT_DIR / "docs"
MLRUNS_DIR = ROOT_DIR / "mlruns"

ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

TARGET_CATEGORIES = [
    "bank_kyc_account",
    "upi_payment",
    "cashback_reward_lottery",
    "job",
    "investment",
    "loan",
    "delivery",
    "gov_police_impersonation",
    "tech_support",
    "other",
]


def load_sms_dataset() -> tuple[list[str], list[int]]:
    """Loads UCI SMS Spam Collection file."""
    sms_path = ML_DATA_DIR / "raw" / "sms" / "SMSSpamCollection"
    if not sms_path.exists():
        raise FileNotFoundError(f"SMS dataset not found at {sms_path}")

    texts: list[str] = []
    labels: list[int] = []
    with open(sms_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t", 1)
            if len(parts) == 2:
                label_str, text = parts
                labels.append(1 if label_str.strip().lower() == "spam" else 0)
                texts.append(text.strip())

    logger.info(f"Loaded {len(texts)} SMS messages (Spam={sum(labels)}, Ham={len(labels)-sum(labels)})")
    return texts, labels


def train_binary_models(texts: list[str], labels: list[int]) -> dict:
    """Trains and compares 6 binary classifiers with MLflow tracking."""
    mlflow.set_tracking_uri(str(MLRUNS_DIR))
    mlflow.set_experiment("scamshield_text_binary")

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        strip_accents="unicode",
        lowercase=True,
    )
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)

    models = {
        "LogisticRegression": LogisticRegression(
            C=1.0, max_iter=1000, class_weight="balanced", random_state=42
        ),
        "KNeighbors": KNeighborsClassifier(
            n_neighbors=5, weights="distance"
        ),
        "DecisionTree": DecisionTreeClassifier(
            max_depth=20, random_state=42
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1
        ),
        "SVM_Linear": SVC(
            kernel="linear", probability=True, class_weight="balanced", random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            eval_metric="logloss",
            random_state=42,
        ),
    }

    results: dict[str, dict] = {}
    best_model_name: str | None = None
    best_recall = -1.0
    best_fpr = 1.0

    for name, clf in models.items():
        logger.info(f"Training binary model: {name}...")
        start_time = time.time()
        clf.fit(X_train, y_train)
        train_time = round(time.time() - start_time, 4)

        y_pred = clf.predict(X_test)
        if hasattr(clf, "predict_proba"):
            y_proba = clf.predict_proba(X_test)[:, 1]
        else:
            y_proba = y_pred

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

        try:
            auc = float(roc_auc_score(y_test, y_proba))
        except Exception:
            auc = 0.0

        metrics = {
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(auc, 4),
            "fpr": round(fpr, 4),
            "fnr": round(fnr, 4),
            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn),
            "train_time_sec": train_time,
        }
        results[name] = metrics

        with mlflow.start_run(run_name=f"binary_{name}"):
            mlflow.log_param("model_family", name)
            mlflow.log_param("vectorizer", "TfidfVectorizer(1,2)")
            mlflow.log_param("max_features", 5000)
            mlflow.log_metrics(metrics)

        # Select by recall with acceptable FPR (<= 0.05)
        if fpr <= 0.05:
            if rec > best_recall or (rec == best_recall and fpr < best_fpr):
                best_recall = rec
                best_fpr = fpr
                best_model_name = name

    # Fallback if no model had FPR <= 0.05
    if best_model_name is None:
        best_model_name = max(results.keys(), key=lambda k: results[k]["recall"])

    logger.info(f"Selected best binary text model: {best_model_name} (Recall: {results[best_model_name]['recall']}, FPR: {results[best_model_name]['fpr']})")

    # Retrain best model on full dataset
    logger.info(f"Retraining {best_model_name} on entire UCI SMS dataset...")
    full_vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        sublinear_tf=True,
        strip_accents="unicode",
        lowercase=True,
    )
    X_full = full_vectorizer.fit_transform(texts)
    best_clf = models[best_model_name]
    best_clf.fit(X_full, labels)

    save_payload = {
        "model_name": best_model_name,
        "vectorizer": full_vectorizer,
        "classifier": best_clf,
        "metrics": results[best_model_name],
    }
    model_path = ARTIFACTS_DIR / "text_binary_model.joblib"
    joblib.dump(save_payload, model_path)
    logger.info(f"Saved binary model artifact to {model_path}")

    return {
        "comparison": results,
        "selected_model": best_model_name,
        "selected_metrics": results[best_model_name],
    }


def train_category_models() -> dict:
    """Trains and compares Category models on synthetic data evaluated on handwritten test set."""
    mlflow.set_tracking_uri(str(MLRUNS_DIR))
    mlflow.set_experiment("scamshield_category_multiclass")

    syn_path = ML_DATA_DIR / "synthetic" / "synthetic_scams.csv"
    test_path = ML_DATA_DIR / "handwritten_test.csv"

    if not syn_path.exists():
        raise FileNotFoundError(f"Synthetic data not found at {syn_path}")
    if not test_path.exists():
        raise FileNotFoundError(f"Handwritten test set not found at {test_path}")

    syn_df = pd.read_csv(syn_path)
    test_df = pd.read_csv(test_path)

    # Filter to the 10 scam classes
    train_df = syn_df[(syn_df["label_scam"].astype(str) == "1") & (syn_df["category"].isin(TARGET_CATEGORIES))].copy()
    eval_df = test_df[(test_df["label_scam"].astype(str) == "1") & (test_df["category"].isin(TARGET_CATEGORIES))].copy()

    logger.info(f"Category training set: {len(train_df)} rows across {train_df['category'].nunique()} categories")
    logger.info(f"Category evaluation benchmark: {len(eval_df)} rows across {eval_df['category'].nunique()} categories")

    le = LabelEncoder()
    le.fit(TARGET_CATEGORIES)

    y_train = le.transform(train_df["category"])
    y_test = le.transform(eval_df["category"])

    train_texts = train_df["text"].tolist()
    test_texts = eval_df["text"].tolist()

    category_results: dict[str, dict] = {}

    # Model 1: TF-IDF + Logistic Regression
    logger.info("Training Model 1: TF-IDF + Logistic Regression...")
    tfidf = TfidfVectorizer(ngram_range=(1, 2), max_features=5000, sublinear_tf=True)
    X_train_tfidf = tfidf.fit_transform(train_texts)
    X_test_tfidf = tfidf.transform(test_texts)

    lr_tfidf = LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", random_state=42)
    start_t = time.time()
    lr_tfidf.fit(X_train_tfidf, y_train)
    t_tfidf = round(time.time() - start_t, 4)

    y_pred_tfidf = lr_tfidf.predict(X_test_tfidf)
    acc_tfidf = float(accuracy_score(y_test, y_pred_tfidf))
    f1_macro_tfidf = float(f1_score(y_test, y_pred_tfidf, average="macro", zero_division=0))
    prec_macro_tfidf = float(precision_score(y_test, y_pred_tfidf, average="macro", zero_division=0))
    rec_macro_tfidf = float(recall_score(y_test, y_pred_tfidf, average="macro", zero_division=0))

    metrics_tfidf = {
        "accuracy": round(acc_tfidf, 4),
        "f1_macro": round(f1_macro_tfidf, 4),
        "precision_macro": round(prec_macro_tfidf, 4),
        "recall_macro": round(rec_macro_tfidf, 4),
        "train_time_sec": t_tfidf,
    }
    category_results["TF-IDF + LogisticRegression"] = metrics_tfidf

    with mlflow.start_run(run_name="category_tfidf_logistic_regression"):
        mlflow.log_param("representation", "TF-IDF (1,2)")
        mlflow.log_param("classifier", "LogisticRegression")
        mlflow.log_metrics(metrics_tfidf)

    # Model 2: MiniLM Embeddings + Logistic Regression
    logger.info("Computing MiniLM embeddings (all-MiniLM-L6-v2)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    X_train_emb = embedder.encode(train_texts, show_progress_bar=False, normalize_embeddings=True)
    X_test_emb = embedder.encode(test_texts, show_progress_bar=False, normalize_embeddings=True)

    logger.info("Training Model 2: MiniLM Embeddings + Logistic Regression...")
    lr_emb = LogisticRegression(C=1.0, max_iter=1000, class_weight="balanced", random_state=42)
    start_t = time.time()
    lr_emb.fit(X_train_emb, y_train)
    t_emb = round(time.time() - start_t, 4)

    y_pred_emb = lr_emb.predict(X_test_emb)
    acc_emb = float(accuracy_score(y_test, y_pred_emb))
    f1_macro_emb = float(f1_score(y_test, y_pred_emb, average="macro", zero_division=0))
    prec_macro_emb = float(precision_score(y_test, y_pred_emb, average="macro", zero_division=0))
    rec_macro_emb = float(recall_score(y_test, y_pred_emb, average="macro", zero_division=0))

    metrics_emb = {
        "accuracy": round(acc_emb, 4),
        "f1_macro": round(f1_macro_emb, 4),
        "precision_macro": round(prec_macro_emb, 4),
        "recall_macro": round(rec_macro_emb, 4),
        "train_time_sec": t_emb,
    }
    category_results["MiniLM + LogisticRegression"] = metrics_emb

    with mlflow.start_run(run_name="category_minilm_logistic_regression"):
        mlflow.log_param("representation", "all-MiniLM-L6-v2")
        mlflow.log_param("classifier", "LogisticRegression")
        mlflow.log_metrics(metrics_emb)

    # Pick best category model based on f1_macro on the test set
    if f1_macro_emb >= f1_macro_tfidf:
        best_cat_name = "MiniLM + LogisticRegression"
        best_payload = {
            "model_type": "minilm_embeddings",
            "embedder_name": "all-MiniLM-L6-v2",
            "classifier": lr_emb,
            "classes": TARGET_CATEGORIES,
            "metrics": metrics_emb,
        }
    else:
        best_cat_name = "TF-IDF + LogisticRegression"
        best_payload = {
            "model_type": "tfidf",
            "vectorizer": tfidf,
            "classifier": lr_tfidf,
            "classes": TARGET_CATEGORIES,
            "metrics": metrics_tfidf,
        }

    logger.info(f"Selected best category model: {best_cat_name} (Macro F1: {category_results[best_cat_name]['f1_macro']})")

    cat_model_path = ARTIFACTS_DIR / "category_model.joblib"
    joblib.dump(best_payload, cat_model_path)
    logger.info(f"Saved category model artifact to {cat_model_path}")

    return {
        "comparison": category_results,
        "selected_model": best_cat_name,
        "selected_metrics": category_results[best_cat_name],
    }


def write_eval_markdown(binary_res: dict, category_res: dict):
    """Writes evaluation metrics and model comparison to docs/EVAL.md."""
    eval_file = DOCS_DIR / "EVAL.md"

    b_comp = binary_res["comparison"]
    c_comp = category_res["comparison"]

    md = """# ScamShield AI — Model Evaluation & Benchmarks

*Generated automatically by `ml/training/train_text_models.py` with tracking logged to MLflow.*

## 1. Binary Text Scam / Ham Classification

- **Dataset**: UCI SMS Spam Collection (5,574 rows)
- **Split**: 80% Train, 20% Stratified Test Holdout
- **Features**: TF-IDF (`ngram_range=(1,2)`, `max_features=5000`, `sublinear_tf=True`)
- **Optimization Strategy**: Recall prioritization at acceptable FPR (FPR $\\le$ 0.05) per Principle #5.

### Model Comparison Table

| Model | Accuracy | Precision | Recall (TPR) | F1-Score | ROC-AUC | FPR | FNR | Train Time (s) |
|---|---|---|---|---|---|---|---|---|
"""
    for model_name, m in b_comp.items():
        is_sel = " **(Selected)**" if model_name == binary_res["selected_model"] else ""
        md += f"| **{model_name}**{is_sel} | {m['accuracy']:.4f} | {m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} | {m['roc_auc']:.4f} | {m['fpr']:.4f} | {m['fnr']:.4f} | {m['train_time_sec']:.2f} |\n"

    b_best = binary_res["selected_metrics"]
    md += f"""
### Selected Binary Model: `{binary_res['selected_model']}`
- **Test Confusion Matrix**: TP={b_best['tp']}, FP={b_best['fp']}, TN={b_best['tn']}, FN={b_best['fn']}
- **False Negative Rate (FNR)**: {b_best['fnr'] * 100:.2f}%
- **False Positive Rate (FPR)**: {b_best['fpr'] * 100:.2f}%
- **Decision Rationale**: Maximizes safety by minimizing missed scams (high Recall) while maintaining acceptable false alarm rate.

---

## 2. Multi-Class Scam Category Classification (10 Categories)

- **Training Data**: Synthetic Scam Corpus (`ml/data/synthetic/synthetic_scams.csv`, 1,000 scam messages across 10 classes)
- **Evaluation Benchmark**: Handwritten Test Set (`ml/data/handwritten_test.csv`, 40 held-out Indian scam messages, 4 per class)
- **Target Classes**: `bank_kyc_account`, `upi_payment`, `cashback_reward_lottery`, `job`, `investment`, `loan`, `delivery`, `gov_police_impersonation`, `tech_support`, `other`.

### Representation & Model Comparison

| Representation + Classifier | Accuracy | Macro Precision | Macro Recall | Macro F1 | Train Time (s) |
|---|---|---|---|---|---|
"""
    for cat_name, m in c_comp.items():
        is_sel = " **(Selected)**" if cat_name == category_res["selected_model"] else ""
        md += f"| **{cat_name}**{is_sel} | {m['accuracy']:.4f} | {m['precision_macro']:.4f} | {m['recall_macro']:.4f} | {m['f1_macro']:.4f} | {m['train_time_sec']:.2f} |\n"

    md += f"""
### Selected Category Model: `{category_res['selected_model']}`
- **Evaluation Benchmark Performance**: Macro F1: {category_res['selected_metrics']['f1_macro']:.4f}, Accuracy: {category_res['selected_metrics']['accuracy']:.4f}.
- **Artifact**: `ml/artifacts/category_model.joblib`

---

## 3. MLflow Local Tracking
All parameters, metrics, and runs are tracked in local MLflow directory (`mlruns`).
To view the interactive MLflow UI dashboard:
```powershell
.\\.venv\\Scripts\\python.exe -m mlflow ui
```
Navigate to: `http://localhost:5000`
"""
    with open(eval_file, "w", encoding="utf-8") as f:
        f.write(md)

    logger.info(f"Evaluation report written to {eval_file}")


def main():
    logger.info("=== Starting ScamShield Text Model Training & Comparison ===")
    texts, labels = load_sms_dataset()
    binary_res = train_binary_models(texts, labels)

    logger.info("=== Starting Category Model Comparison ===")
    category_res = train_category_models()

    write_eval_markdown(binary_res, category_res)

    summary = {
        "binary_comparison": binary_res,
        "category_comparison": category_res,
    }
    with open(ARTIFACTS_DIR / "model_comparison_metrics.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info("=== Training and evaluation complete! ===")
    print("\n" + "=" * 60)
    print(f"BEST BINARY MODEL:   {binary_res['selected_model']}")
    print(f"  Recall:            {binary_res['selected_metrics']['recall']}")
    print(f"  FPR:               {binary_res['selected_metrics']['fpr']}")
    print(f"  ROC-AUC:           {binary_res['selected_metrics']['roc_auc']}")
    print(f"BEST CATEGORY MODEL: {category_res['selected_model']}")
    print(f"  Macro F1:          {category_res['selected_metrics']['f1_macro']}")
    print(f"  Accuracy:          {category_res['selected_metrics']['accuracy']}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
