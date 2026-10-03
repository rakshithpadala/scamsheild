# ScamShield AI — Project Report Tables & Technical Appendix
*Exported per Template R6 for Mumbai University BE/BTech AI/ML Project Report & Viva Documentation.*

---

## 1. Binary Text Model Comparison (UCI SMS Spam Holdout)

- **Dataset**: UCI SMS Spam Collection (5,574 rows; 4,827 Ham, 747 Spam)
- **Split**: 80% Train, 20% Stratified Test Holdout
- **Feature Pipeline**: TF-IDF (`ngram_range=(1,2)`, `max_features=5000`, `sublinear_tf=True`)
- **Optimization Strategy**: Recall prioritization at acceptable FPR ($\le 0.05$) per Principle #5.

| Model Family | Accuracy | Precision | Recall (TPR) | F1-Score | ROC-AUC | FPR | FNR | Train Time (s) | Selection Status |
|---|---|---|---|---|---|---|---|---|---|
| **Logistic Regression** | **0.9839** | **0.9396** | **0.9396** | **0.9396** | **0.9920** | **0.0093** | **0.0604** | **0.10** | **SELECTED** |
| Support Vector Machine (Linear) | 0.9874 | 0.9720 | 0.9329 | 0.9521 | 0.9896 | 0.0041 | 0.0671 | 16.61 | Evaluated |
| Random Forest | 0.9794 | 1.0000 | 0.8456 | 0.9164 | 0.9930 | 0.0000 | 0.1544 | 1.67 | Evaluated |
| XGBoost | 0.9821 | 0.9850 | 0.8792 | 0.9291 | 0.9817 | 0.0021 | 0.1208 | 17.95 | Evaluated |
| Decision Tree | 0.9722 | 0.9338 | 0.8523 | 0.8912 | 0.8881 | 0.0093 | 0.1477 | 0.50 | Evaluated |
| K-Nearest Neighbors (k=5) | 0.9516 | 0.9897 | 0.6443 | 0.7805 | 0.8612 | 0.0010 | 0.3557 | 0.01 | Evaluated |

### Selected Binary Model Confusion Matrix (Test Set: N = 1,115)
- **True Positives (TP)**: 140
- **False Positives (FP)**: 9
- **True Negatives (TN)**: 957
- **False Negatives (FN)**: 9
- **False Negative Rate (FNR)**: 6.04%

---

## 2. Multi-Class Scam Category Model Results (10 Classes)

- **Training Corpus**: Calibrated Synthetic Indian Scam Messages ($N = 1,000$ scam samples, 100 per category)
- **Evaluation Benchmark**: Independent Handwritten Test Set ($N = 40$ held-out Indian scam messages, 4 per category)
- **Target Classes**: `bank_kyc_account`, `upi_payment`, `cashback_reward_lottery`, `job`, `investment`, `loan`, `delivery`, `gov_police_impersonation`, `tech_support`, `other`.

| Representation + Classifier | Test Accuracy | Macro Precision | Macro Recall | Macro F1 | Train Time (s) | Selection Status |
|---|---|---|---|---|---|---|
| **TF-IDF (1,2) + Logistic Regression** | **0.8250** | **0.8400** | **0.8250** | **0.8124** | **1.05** | **SELECTED** |
| SentenceTransformer (all-MiniLM-L6-v2) + LR | 0.8000 | 0.8267 | 0.8000 | 0.7892 | 2.76 | Evaluated |

---

## 3. URL Lexical Model Comparison

*Evaluated on Tranco Top-1M (Benign) vs OpenPhish + URLhaus (Malicious) split by registered domain (GroupShuffleSplit).*

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
|---|---|---|---|---|---|---|
| Logistic Regression | MISSING | MISSING | MISSING | MISSING | MISSING | Scheduled Day 3 |
| Random Forest | MISSING | MISSING | MISSING | MISSING | MISSING | Scheduled Day 3 |
| XGBoost + SHAP | MISSING | MISSING | MISSING | MISSING | MISSING | Scheduled Day 3 |

---

## 4. Calibrated Multi-Modal Fusion Engine Weights

| Signal Source | Modality | Output Range | Weight in Fusion | Behavior & Edge-Case Handling |
|---|---|---|---|---|
| **Threat Intel Match** | URL / Hash | `match` / `no_match` / `unavailable` | **Override (1.00)** | Verified OpenPhish / URLhaus match forces verdict `KNOWN_THREAT` and risk score $\ge 95$. `unavailable` never treated as safe. |
| **Rule Engine** | Text / Email | 0.00 – 1.00 (Weighted Spans) | **0.45** | Deterministic detection for urgent extortion, UPI PIN traps, and digital arrest threats. Generates highlighted text spans. |
| **Statistical NLP Model** | Text | 0.00 – 1.00 (Probability) | **0.35** | Calibrated TF-IDF + Logistic Regression scam probability score. Detects novel wording. |
| **Lexical URL Model** | URL features | 0.00 – 1.00 (Risk Score) | **0.20** | 25+ domain and path lexical features (entropy, IP host, punycode, TLD suspiciousness). |
| **Short / Blank Text** | Metadata | Character count < 15 | **Override (N/A)** | Automatically sets verdict to `INSUFFICIENT_EVIDENCE`. |

---

## 5. Mumbai University AI/ML Syllabus Mapping Table

| Syllabus Module / Concept | Academic Syllabus Topic | ScamShield Implementation in Project | Artifact / Code Location |
|---|---|---|---|
| **Supervised Learning: Classification** | Linear Classifiers, Decision Trees, Ensembles, SVM | Comparative evaluation of 6 classifiers (LR, KNN, DT, RF, SVM, XGBoost) on SMS Spam with Recall prioritization | `ml/training/train_text_models.py`, `docs/EVAL.md` |
| **Multi-Class Classification & NLP** | Text Representation, TF-IDF, Vector Space Models | 10-class scam categorization comparing sparse TF-IDF n-grams against dense MiniLM sentence embeddings | `ml/training/train_text_models.py`, `backend/app/ml/` |
| **Model Evaluation Metrics** | Confusion Matrix, ROC-AUC, Precision, Recall, F1 | Comprehensive evaluation optimizing for recall at acceptable FPR ($\le 0.05$); error analysis on false negatives | `docs/EVAL.md`, `mlruns/` |
| **Unsupervised Learning: Clustering** | K-Means, Agglomerative Hierarchical, Silhouette Score | Clustering scam narrative patterns and evaluating cluster cohesion via silhouette coefficient | `ml/notebooks/01_clustering.ipynb` |
| **Dimensionality Reduction** | Principal Component Analysis (PCA) | 2D PCA projection of high-dimensional TF-IDF vectors to visualize scam vs legitimate message separation | `ml/notebooks/02_pca.ipynb` |
| **Association Rule Mining** | Apriori Algorithm, Support, Confidence, Lift | Mining co-occurrence patterns between fraud indicators (e.g., OTP request + urgency + external link) | `ml/notebooks/03_apriori.ipynb` |
| **Regression Analysis** | Linear & Ridge Regression, Regularization | Score calibration and continuous risk index estimation (MAE, $R^2$ metrics) | `ml/notebooks/04_regression.ipynb` |
| **Search & Graph Algorithms** | BFS, DFS, Uniform Cost Search, Greedy, A* Search | Threat path exploration across an entity fraud graph (UPI IDs, phone numbers, domain nodes) | `ml/notebooks/05_graph_search.ipynb` |
| **Information Retrieval & RAG** | Vector Databases, Cosine Similarity, Embeddings | Retrieval-Augmented Generation retrieving official safety guidance from RBI, NPCI, and I4C advisories | `knowledge_base/`, `backend/app/rag/` |
| **Computer Vision / OCR** | Image Preprocessing, Binarization, Character Recognition | OpenCV preprocessing (grayscale, bilateral filter, adaptive threshold) + Tesseract OCR | `backend/app/services/ocr.py` |

---

## 6. Backend API Endpoints Contract

| Method | Route | Request Schema | Response Schema | Purpose |
|---|---|---|---|---|
| `GET` | `/health` | None | `{"status": "ok", "version": "0.1.0"}` | Healthcheck and container liveness probe |
| `POST` | `/analyze/message` | `MessageRequest(text: str)` | `AnalysisResult` | Main text message fraud detection & evidence fusion |
| `POST` | `/api/analyze` | `MessageRequest(text: str)` | `AnalysisResult` | Frontend API compatibility route |
| `GET` | `/analyze/stream/{id}`| SSE Stream | `StreamStage(stage, progress)` | Server-Sent Events real-time analysis progress stepper |
| `GET` | `/analysis/{id}` | None | `AnalysisResult` | Retrieve historical analysis by unique UUID |
| `GET` | `/analysis/history` | Query params `(limit, offset)` | `list[AnalysisHistoryItem]` | Paginated past scan history |
| `POST` | `/copilot/chat` | `CopilotRequest(query: str)` | `CopilotResponse` | Context-aware RAG safety copilot assistant |
| `GET` | `/models/metrics` | None | `ModelMetricsResponse` | Real-time performance metrics for UI Model Lab |
