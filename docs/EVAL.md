# ScamShield AI — Model Evaluation & Benchmarks

*Generated automatically by `ml/training/train_text_models.py` with tracking logged to MLflow.*

## 1. Binary Text Scam / Ham Classification

- **Dataset**: UCI SMS Spam Collection (5,574 rows)
- **Split**: 80% Train, 20% Stratified Test Holdout
- **Features**: TF-IDF (`ngram_range=(1,2)`, `max_features=5000`, `sublinear_tf=True`)
- **Optimization Strategy**: Recall prioritization at acceptable FPR (FPR $\le$ 0.05) per Principle #5.

### Model Comparison Table

| Model | Accuracy | Precision | Recall (TPR) | F1-Score | ROC-AUC | FPR | FNR | Train Time (s) |
|---|---|---|---|---|---|---|---|---|
| **LogisticRegression** **(Selected)** | 0.9839 | 0.9396 | 0.9396 | 0.9396 | 0.9920 | 0.0093 | 0.0604 | 0.10 |
| **KNeighbors** | 0.9516 | 0.9897 | 0.6443 | 0.7805 | 0.8612 | 0.0010 | 0.3557 | 0.01 |
| **DecisionTree** | 0.9722 | 0.9338 | 0.8523 | 0.8912 | 0.8881 | 0.0093 | 0.1477 | 0.50 |
| **RandomForest** | 0.9794 | 1.0000 | 0.8456 | 0.9164 | 0.9930 | 0.0000 | 0.1544 | 1.67 |
| **SVM_Linear** | 0.9874 | 0.9720 | 0.9329 | 0.9521 | 0.9896 | 0.0041 | 0.0671 | 16.61 |
| **XGBoost** | 0.9821 | 0.9850 | 0.8792 | 0.9291 | 0.9817 | 0.0021 | 0.1208 | 17.95 |

### Selected Binary Model: `LogisticRegression`
- **Test Confusion Matrix**: TP=140, FP=9, TN=957, FN=9
- **False Negative Rate (FNR)**: 6.04%
- **False Positive Rate (FPR)**: 0.93%
- **Decision Rationale**: Maximizes safety by minimizing missed scams (high Recall) while maintaining acceptable false alarm rate.

---

## 2. Multi-Class Scam Category Classification (10 Categories)

- **Training Data**: Synthetic Scam Corpus (`ml/data/synthetic/synthetic_scams.csv`, 1,000 scam messages across 10 classes)
- **Evaluation Benchmark**: Handwritten Test Set (`ml/data/handwritten_test.csv`, 40 held-out Indian scam messages, 4 per class)
- **Target Classes**: `bank_kyc_account`, `upi_payment`, `cashback_reward_lottery`, `job`, `investment`, `loan`, `delivery`, `gov_police_impersonation`, `tech_support`, `other`.

### Representation & Model Comparison

| Representation + Classifier | Accuracy | Macro Precision | Macro Recall | Macro F1 | Train Time (s) |
|---|---|---|---|---|---|
| **TF-IDF + LogisticRegression** **(Selected)** | 0.8250 | 0.8400 | 0.8250 | 0.8124 | 1.05 |
| **MiniLM + LogisticRegression** | 0.8000 | 0.8267 | 0.8000 | 0.7892 | 2.76 |

### Selected Category Model: `TF-IDF + LogisticRegression`
- **Evaluation Benchmark Performance**: Macro F1: 0.8124, Accuracy: 0.8250.
- **Artifact**: `ml/artifacts/category_model.joblib`

---

## 3. MLflow Local Tracking
All parameters, metrics, and runs are tracked in local MLflow directory (`mlruns`).
To view the interactive MLflow UI dashboard:
```powershell
.\.venv\Scripts\python.exe -m mlflow ui
```
Navigate to: `http://localhost:5000`
