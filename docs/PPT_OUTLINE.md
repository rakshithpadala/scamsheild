# ScamShield AI — 14-Slide Presentation Outline (Task T16)
*Designed for Mumbai University Final Year BE/BTech AI/ML Project Presentation & Viva (14 slides, max 3 bullets per slide).*

---

### Slide 1: Title & Project Identity
- **Title**: ScamShield AI — Multimodal Personal Digital-Safety Assistant (India-Focused)
- **Institution**: University of Mumbai | Department of Computer Engineering / AI & ML
- **Philosophy**: *Detect → Investigate → Explain → Verify → Act Safely*

---

### Slide 2: Problem Statement & Indian Cyber Threat Landscape
- Escalation of tailored social engineering attacks in India: UPI PIN collect traps, fake KYC deactivations, and forged "Digital Arrest" extortion.
- Inadequacy of binary spam filters: existing tools flag "spam" without explaining the trap mechanism or providing actionable, cited relief steps.
- Critical citizen vulnerability: high financial loss rates among non-technical and elderly users unaware of UPI architecture.

---

### Slide 3: Objectives & Core Contributions
- Deliver a unified multi-modal detection engine accepting SMS text, device screenshots, raw URLs, and forwarded email headers.
- Enforce evidence-based explainability with highlighted suspicious text spans and official citations (RBI, NPCI, I4C).
- Prioritize detection recall over simple accuracy: minimizing missed fraud (false negatives) while keeping false alarm rate $\le 1\%$.

---

### Slide 4: End-to-End System Architecture
- **Input & Extraction**: Tesseract OCR for screenshots, regex-based entity extractors for UPI handles, URLs, and phone numbers.
- **Parallel Analysis Core**: Statistical NLP classifier, 10-class category model, 12+ rule triggers, and live threat feed lookups.
- **Calibrated Fusion & Presentation**: Weighted risk aggregator (0–100), RAG guidance vector store, and React security command center.

---

### Slide 5: Datasets & Research Honesty Statement
- **Foundational Baselines**: UCI SMS Spam Collection (5,574 messages), Tranco Top-1M benign domains, OpenPhish & URLhaus feeds.
- **Indian Fraud Taxonomy**: 1,000 calibrated synthetic Indian scam samples across 10 classes (UPI, KYC, Job, Digital Arrest, Loans).
- **Gold Evaluation Benchmark**: 60-row hand-crafted test set (40 realistic Indian scams + 20 benign hard negatives, no data leakage).

---

### Slide 6: Binary Text Scam Detection (UCI SMS Benchmark)
- Benchmarked 6 algorithms: Logistic Regression, Linear SVM, Random Forest, XGBoost, Decision Tree, and K-Nearest Neighbors.
- Selected Logistic Regression for production: **93.96% Recall** at **0.93% FPR** with **0.9920 ROC-AUC** and ultra-low 0.10s latency.
- Strict avoidance of accuracy-only traps: high recall ensures dangerous extortion messages are rarely missed.

---

### Slide 7: 10-Class Scam Category Classification
- Merged taxonomy addressing India's most prevalent scams: Bank KYC, UPI Collect, Cashback/Lottery, Job, Investment, Loan, Delivery, Police, Tech Support.
- Evaluated Sparse TF-IDF n-grams (1,2) vs Dense SentenceTransformer (`all-MiniLM-L6-v2`) on the independent handwritten benchmark.
- Selected TF-IDF + Logistic Regression: achieves **82.50% Test Accuracy** and **0.8124 Macro F1** with minimal memory footprint.

---

### Slide 8: Deterministic Rule Engine & Threat Intelligence
- 12+ expert rules capturing urgency threats, account suspension, UPI PIN entry triggers, and legal extortion keywords.
- Generates exact character spans and confidence weights, providing direct visual feedback in the user interface.
- Zero-day threat feed cache matching against OpenPhish and URLhaus; confirmed feeds trigger immediate `KNOWN_THREAT` override.

---

### Slide 9: Calibrated Multi-Modal Risk Fusion Engine
- Transparent weighted linear combination: Rules (0.45) + Statistical ML (0.35) + Lexical URL (0.20) with Threat Intel override.
- Discrete, unambiguous verdicts: `KNOWN_THREAT` (95–100), `SUSPICIOUS` (60–94), `LOW_RISK` (0–30), `INSUFFICIENT_EVIDENCE`.
- SSRF-safe by design: submitted links are lexically inspected without server-side HTTP rendering.

---

### Slide 10: Retrieval-Augmented Generation (RAG) & Emergency Guidance
- Local NumPy+JSON vector store indexing official advisories from Reserve Bank of India (RBI), NPCI, and Indian Cyber Crime Coordination Centre (I4C).
- Plain-language safety instructions emphasizing fundamental banking truths (e.g., "UPI PIN is never required to receive money").
- Automatic surfacing of the National Cyber Crime Helpline (**1930**) and portal (**cybercrime.gov.in**) if money is at risk.

---

### Slide 11: Security Command Center Frontend
- Calm, accessible dark-first interface styled with Tailwind CSS, Radix UI primitives, and Framer Motion animations.
- Four-level visual risk gauge with WCAG AA-compliant status badges and interactive evidence progress bars.
- Dedicated tabs for Text Scanner, Screenshot OCR with side-by-side editable text, URL Inspector, and RAG Copilot drawer.

---

### Slide 12: Mumbai University Syllabus Implementation
- **Supervised ML**: 6 binary classifiers + multi-class category models with full hyperparameter tuning and MLflow tracking.
- **Unsupervised ML & Dimensionality Reduction**: K-Means & Hierarchical clustering of threat narratives; 2D PCA feature projection.
- **Association Mining & Graph Algorithms**: Apriori indicator co-occurrence; BFS/DFS/A* shortest threat path search over entity graphs.

---

### Slide 13: Ethics, Safety Guarantees & Limitations
- **Credential Protection**: System never requests, captures, or persists UPI PINs, passwords, or OTPs.
- **LLM Boundary**: The language model never determines verdicts; verdicts derive purely from deterministic rules and ML evidence.
- **Humility & Non-Overclaiming**: System reports "high-risk characteristics detected", never "definitely a scam", accompanied by explicit limitations.

---

### Slide 14: Demonstration, Viva Takeaways & Future Work
- Live demonstration flow: analyzing a UPI cashback collect trap, a fake police digital arrest notice, and a benign bank transaction OTP.
- Containerized reproducibility: clean-clone zero-configuration deployment via `docker compose up --build`.
- Future roadmap: on-device lightweight mobile SDK, multilingual Indian vernacular support (Hindi, Marathi, Tamil), and pgvector scaling.
