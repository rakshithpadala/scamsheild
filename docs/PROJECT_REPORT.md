# ScamShield AI: A Multi-Modal Personal Digital Safety Assistant
**University of Mumbai — Department of Computer Engineering / Artificial Intelligence & Machine Learning**  
*Final Year BE / BTech Capstone Project Report & Technical Documentation*

---

## Executive Summary / Abstract

With India's exponential adoption of digital public infrastructure—specifically the Unified Payments Interface (UPI)—cyber fraud techniques have evolved from crude lottery phishing into sophisticated, hyper-targeted social engineering attacks. Prevalent fraud typologies include coercive UPI PIN collect traps disguised as cashbacks, fraudulent account suspension threats (fake KYC expiry), and psychological extortion masquerading as law enforcement "Digital Arrests". Existing automated security solutions suffer from critical shortcomings: binary spam filters provide uncalibrated flags without explaining the deception mechanism, while general-purpose large language models (LLMs) hallucinate verdicts and risk exposure of sensitive financial credentials.

**ScamShield AI** is an intelligent, multi-modal personal digital-safety assistant tailored to the Indian threat landscape. Following the foundational design philosophy: **Detect → Investigate → Explain → Verify → Act Safely**, the platform ingests heterogeneous user inputs (SMS text, device screenshots via Tesseract OCR, suspicious URLs, and email headers). Rather than relying on non-deterministic LLM decision-making, the system employs a deterministic, transparent multi-modal architecture comprising:
1. A calibrated statistical Natural Language Processing (NLP) classifier;
2. A 10-class scam category categorization model;
3. A deterministic heuristic rule engine evaluating 12+ expert threat patterns and highlighting exact character spans;
4. Real-time threat intelligence matching against active feeds (OpenPhish and URLhaus);
5. A calibrated fusion aggregator yielding a 0–100 risk score and four discrete verdicts (`KNOWN_THREAT`, `SUSPICIOUS`, `LOW_RISK`, `INSUFFICIENT_EVIDENCE`);
6. A Retrieval-Augmented Generation (RAG) guidance copilot indexing official advisories from the Reserve Bank of India (RBI), National Payments Corporation of India (NPCI), and Indian Cyber Crime Coordination Centre (I4C).

Benchmarked across 5,574 UCI SMS Spam records and an independent 60-row hand-crafted Indian test benchmark, ScamShield AI achieves **93.96% Recall** at **0.93% False Positive Rate (FPR)** with an ROC-AUC of **0.9920** for binary threat detection, and **82.50% Accuracy** (0.8124 Macro F1) across 10 fine-grained scam categories. The system enforces strict credential-safety guardrails: it never requests or stores UPI PINs, passwords, or OTPs, and programmatically routes compromised citizens to the National Cyber Crime Helpline (**1930**) and portal (**cybercrime.gov.in**).

---

## 1. Problem Statement & Motivation

### 1.1 The Indian Cyber Threat Landscape
Digital payment transactions in India exceed 13 billion monthly transactions via UPI. This unprecedented velocity has created high-yield attack vectors for cybercriminals targeting non-technical and vulnerable demographics:
- **UPI PIN Collect Trap**: Fraudsters exploit widespread confusion regarding UPI debit versus credit semantics. Victims are instructed to "enter UPI PIN to receive cashback/refund" or coerced into approving malicious collect requests on mobile payment apps.
- **Digital Arrest Extortion**: Attackers impersonate the Central Bureau of Investigation (CBI), Narcotics Control Bureau (NCB), or Mumbai Police, asserting that a parcel containing contraband has been seized in the victim's name, demanding video-call "interrogations" and fund transfers to "RBI security escrow accounts".
- **Account Suspension / Electricity Cutoff**: Urgent SMS warnings claiming electricity disconnection at 9:30 PM or bank account deactivation due to pending KYC verification, redirecting users to malicious APK downloads or phishing portals.

### 1.2 Limitations of Existing Approaches
1. **Opaque Binary Labels**: Common smartphone dialers and SMS filters categorize messages as "Spam" without identifying whether the threat is benign promotional marketing or dangerous financial extortion.
2. **High False Negative Hazards**: In cybersecurity, missing a scam (False Negative) results in catastrophic financial loss, whereas false alarms (False Positives) cause minor friction. Classical classifiers optimizing purely for overall accuracy fail to maintain acceptable recall on dangerous extortion threats.
3. **Hallucination & Credential Theft in LLMs**: Generative AI tools often fabricate legal advice, overconfidently declare malicious links safe, or inadvertently prompt users to enter OTPs or passwords to "verify" transactions.

---

## 2. Dataset Honesty Statement & Data Engineering

In rigorous academic research, data integrity and transparent methodology are non-negotiable. Real-world Indian cyber extortion messages lack standardized public multi-class academic datasets. Accordingly, ScamShield AI combines established foundational benchmarks with calibrated synthetic generation and an independent, hand-crafted gold evaluation set:

1. **Foundational Binary Baseline**: UCI SMS Spam Collection ($N = 5,574$). Used for benchmarking classical classification architectures on legitimate versus spam communications.
2. **Domain Reputation Baselines**: Tranco Top-1M ($N = 1,000,000$) legitimate domains paired with active malicious feeds from OpenPhish Community ($N = 600$) and URLhaus Abuse.ch ($N = 15,904$).
3. **Calibrated Synthetic Indian Scam Corpus**: $N = 1,000$ synthetic scam messages systematically generated across 10 distinct categories using slot-substitution templates (brands, amounts, regional language cues, urgency drivers) to avoid single-template bias.
4. **Independent Handwritten Benchmark (`ml/data/handwritten_test.csv`)**: $N = 60$ hand-crafted rows (40 realistic Indian scams, 4 per class, plus 20 benign hard negatives such as genuine bank OTP alerts, courier tracking updates, and utility reminders). **Crucially, zero handwritten rows overlap with synthetic training data**, guaranteeing completely uncompromised generalization testing.

---

## 3. Model Evaluation & Benchmarks

All parameters, preprocessing pipelines, and metric trajectories are logged to local MLflow tracking (`mlruns`).

### 3.1 Binary Text Classification (UCI SMS Spam Holdout)
- **Dataset**: UCI SMS Spam Collection (80% Train, 20% Stratified Holdout Test; $N_{test} = 1,115$).
- **Features**: TF-IDF (`ngram_range=(1,2)`, `max_features=5000`, `sublinear_tf=True`).
- **Optimization Strategy**: Recall prioritization at acceptable FPR ($\le 0.05$) per Principle #5.

| Algorithm | Test Accuracy | Precision | Recall (TPR) | F1-Score | ROC-AUC | FPR | FNR | Train Time (s) | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **Logistic Regression** | **0.9839** | **0.9396** | **0.9396** | **0.9396** | **0.9920** | **0.0093** | **0.0604** | **0.10** | **SELECTED** |
| Support Vector Machine (Linear) | 0.9874 | 0.9720 | 0.9329 | 0.9521 | 0.9896 | 0.0041 | 0.0671 | 16.61 | Evaluated |
| Random Forest (n=100) | 0.9794 | 1.0000 | 0.8456 | 0.9164 | 0.9930 | 0.0000 | 0.1544 | 1.67 | Evaluated |
| XGBoost (Depth=6) | 0.9821 | 0.9850 | 0.8792 | 0.9291 | 0.9817 | 0.0021 | 0.1208 | 17.95 | Evaluated |
| Decision Tree (Depth=20) | 0.9722 | 0.9338 | 0.8523 | 0.8912 | 0.8881 | 0.0093 | 0.1477 | 0.50 | Evaluated |
| K-Nearest Neighbors (k=5) | 0.9516 | 0.9897 | 0.6443 | 0.7805 | 0.8612 | 0.0010 | 0.3557 | 0.01 | Evaluated |

**Selected Model Analysis**: Logistic Regression achieves the highest recall (**93.96%**), missing only 9 spam messages out of 149 in the test set (FNR: 6.04%), while restricting false alarms to **0.93%** (9 false positives across 966 legitimate messages). Its training and inference latency (<1ms per request) provides optimal real-time throughput.

---

### 3.2 Multi-Class Scam Category Model Results (10 Classes)
Evaluated strictly on the independent 40-row held-out handwritten benchmark (4 messages per class across 10 categories).

| Representation + Classifier | Test Accuracy | Macro Precision | Macro Recall | Macro F1 | Latency / Resource Profile | Status |
|---|---|---|---|---|---|---|
| **TF-IDF (1,2) + Logistic Regression** | **0.8250** | **0.8400** | **0.8250** | **0.8124** | **1.05s train, <1MB RAM** | **SELECTED** |
| SentenceTransformer (all-MiniLM-L6-v2) + LR | 0.8000 | 0.8267 | 0.8000 | 0.7892 | 2.76s train, ~450MB RAM | Evaluated |

**Rationale**: Sparse TF-IDF n-grams slightly outperformed dense 384-dimensional sentence embeddings on localized keyword signals (e.g., "Mudra loan", "e-Challan", "Digital arrest") while operating with negligible CPU and RAM requirements, ensuring zero cold-start latency.

---

## 4. Multi-Modal Architecture & Fusion Engine

ScamShield AI employs a multi-tiered analysis engine:

```
[ Input: SMS / Screenshot / URL / Email ]
                   │
                   ▼
       [ Normalization & Preprocessing ]
       ├── Tesseract OCR (Bilateral Filter + Adaptive Threshold)
       └── Entity Extractor (UPI IDs, URLs, Phone Numbers, Emails)
                   │
    ┌──────────────┼──────────────┬──────────────┐
    ▼              ▼              ▼              ▼
[ Threat Intel ] [ Rule Engine ] [ ML Binary ]  [ ML Category ]
OpenPhish/URLhaus  12+ Heuristics  TF-IDF + LR    10-Class TF-IDF
    │              │              │              │
    └──────────────┼──────────────┴──────────────┘
                   │
                   ▼
     [ Calibrated Risk Fusion Engine ]
     ├── Threat Intel Match  ──► Force KNOWN_THREAT (Score 95-100)
     ├── Linear Combination ──► 0.45*Rules + 0.35*ML + 0.20*URL
     └── Short Input Check   ──► Force INSUFFICIENT_EVIDENCE
                   │
                   ▼
    [ Evidence Aggregator & RAG Copilot ]
    ├── Highlighted Suspicious Spans
    ├── NPCI / RBI Official Citations
    └── Emergency Relief Protocol (1930 / cybercrime.gov.in)
```

### 4.1 Calibrated Fusion Weights Formula
$$\text{RiskScore} = \min\left(100, \left(0.45 \cdot S_{\text{rule}} + 0.35 \cdot P_{\text{ml}} + 0.20 \cdot S_{\text{url}}\right) \times 100\right)$$
- If Threat Intel Feed Match: $\text{Verdict} \leftarrow \text{KNOWN\_THREAT}$, $\text{RiskScore} \leftarrow 98$.
- If $\text{RiskScore} \ge 60$: $\text{Verdict} \leftarrow \text{SUSPICIOUS}$.
- If $\text{RiskScore} < 60$: $\text{Verdict} \leftarrow \text{LOW\_RISK}$.
- If $\text{Length} < 15$ characters and no URL: $\text{Verdict} \leftarrow \text{INSUFFICIENT\_EVIDENCE}$.

---

## 5. Mumbai University Syllabus Mapping Table

| Academic Syllabus Module | Core Subject Concept | ScamShield Project Implementation | Code / Artifact Location |
|---|---|---|---|
| **Supervised Learning** | Linear Models, Ensembles, Support Vector Machines | 6-model benchmark on SMS spam; hyperparameter tuning; recall-centric model selection | `ml/training/train_text_models.py`, `docs/EVAL.md` |
| **Natural Language Processing** | Tokenization, TF-IDF n-grams, Dense Embeddings | Sparse n-gram vectorization vs dense MiniLM sentence embeddings for 10-class fraud taxonomy | `backend/app/ml/`, `ml/artifacts/` |
| **Model Evaluation Metrics** | Confusion Matrix, ROC-AUC, FPR/FNR Tradeoffs | Optimization for Recall at acceptable FPR ($\le 0.05$); full false-negative breakdown | `docs/EVAL.md`, `mlruns/` |
| **Unsupervised Learning** | K-Means & Agglomerative Clustering | Narrative clustering of synthetic fraud templates with silhouette validation | `ml/notebooks/01_clustering.ipynb` |
| **Dimensionality Reduction** | Principal Component Analysis (PCA) | 2D projection of TF-IDF feature space demonstrating linear separability of fraud clusters | `ml/notebooks/02_pca.ipynb` |
| **Association Rule Mining** | Apriori Algorithm, Support, Confidence, Lift | Mining co-occurrence patterns between fraud triggers (urgency + PIN request + shortlink) | `ml/notebooks/03_apriori.ipynb` |
| **Regression Analysis** | Linear & Regularized Ridge Regression | Continuous score calibration and risk index prediction ($R^2$, MAE metrics) | `ml/notebooks/04_regression.ipynb` |
| **AI Search & Graph Theory** | BFS, DFS, Uniform Cost Search, A* Search | Optimal threat path discovery through an entity graph connecting suspect UPIs and phone numbers | `ml/notebooks/05_graph_search.ipynb` |
| **Information Retrieval** | Dense Vector Search, Cosine Similarity, RAG | Vector search across 19 official regulatory PDFs (RBI, NPCI, I4C) for verified mitigation steps | `knowledge_base/`, `backend/app/rag/` |
| **Computer Vision** | Binarization, Noise Reduction, OCR | Bilateral filtering, thresholding, and Tesseract character extraction from mobile screenshots | `backend/app/services/ocr.py` |

---

## 6. Non-Negotiable Safety Principles & Ethical Guardrails

1. **LLM Boundary**: The language model never computes or alters verdicts. Heuristics, ML probability, and verified intel determine the evidence; the LLM merely structures human-readable explanations.
2. **Strict Credential Avoidance**: The system never asks for, records, or logs UPI PINs, banking passwords, CVVs, or OTPs. All logged data strips Personally Identifiable Information (PII).
3. **No Overclaiming**: Analyses use prudent language ("high-risk characteristics detected", never "definitely a scam"). Every result includes an explicit limitations disclaimer.
4. **Emergency Escalation Protocol**: In any incident where money was transferred or accounts compromised, the interface prominently surfaces the Indian National Cyber Crime Helpline (**1930**) and portal (**cybercrime.gov.in**).
5. **SSRF Safety**: Submitted URLs are inspected exclusively via offline lexical heuristics and local feed cache lookups. The server never renders or executes external client code.

---

## 7. Viva Voce Examination Q&A Notes

*High-probability technical questions and model answers for the University Examination Committee:*

#### Q1: Why did you select Logistic Regression over complex ensemble models like XGBoost or Random Forest?
**Answer**: In our empirical benchmark on the UCI SMS Spam dataset, Logistic Regression achieved a higher Recall (**93.96%**) than XGBoost (**87.92%**) and Random Forest (**84.56%**) while maintaining an acceptable False Positive Rate of **0.93%** (FPR $\le 0.05$). In cyber fraud defense, missing a scam (False Negative) is substantially more dangerous than a false alarm. Furthermore, Logistic Regression provides direct linear feature interpretability (coefficients directly highlight suspicious tokens) and executes in 0.10s without GPU requirements.

#### Q2: How did you ensure there is no data leakage between synthetic data and your test set?
**Answer**: We enforced a strict separation of concerns: synthetic data ($N = 1,000$) was generated programmatically using randomized slot templates. In contrast, the evaluation test set ($N = 60$) was hand-written from real-world scam observations and genuine bank notifications. A programmatic verification check in `scripts/validate_my_work.py` computes pairwise normalized string intersections between all synthetic and test texts, verifying an overlap of exactly 0.

#### Q3: Why is the LLM prohibited from determining the risk score or verdict?
**Answer**: LLMs are probabilistic text generators prone to hallucinations, prompt injections, and non-deterministic variability across identical inputs. Allowing an LLM to decide whether a payment request is safe could allow an adversarial message to bypass detection via prompt injection. In ScamShield AI, deterministic rules, trained ML models, and threat intel feeds compute the score; the LLM is restricted to phrasing explanations and indexing verified RAG documents.

#### Q4: Why did sparse TF-IDF outperform dense MiniLM embeddings on category classification?
**Answer**: Indian scam messages rely heavily on localized, high-impact lexical triggers (e.g., "Mudra loan", "e-Challan", "Digital arrest", "UPI collect"). TF-IDF n-grams explicitly capture these exact n-gram signatures. MiniLM embeddings, while semantically rich, occasionally blur distinctions between subtle categories (such as general lottery cashback versus specific UPI collect requests) on shorter SMS messages.

#### Q5: What is the significance of the 1930 helpline in your application?
**Answer**: Under the Ministry of Home Affairs (MHA) Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS), dialling 1930 within the "golden hour" of an unauthorized transaction enables law enforcement to freeze funds across beneficiary accounts before fraudsters can cash out via ATMs or mule accounts. Providing this immediately upon detecting high-risk financial fraud is a vital practical intervention.
