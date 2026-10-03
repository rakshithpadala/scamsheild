# ScamShield Datasets Documentation

## Dataset Honesty Statement
> Scam categories use synthetic data plus a hand-written test set.

Real-world scam messages in the Indian context (specifically targeting UPI fraud, APK drops, KYC deactivation threats, electricity bill scams, and government impersonation) lack standard publicly available multi-class benchmarks. Therefore, fine-grained multi-class classification is trained on calibrated synthetic samples and evaluated against an independent, hand-crafted gold benchmark (`ml/data/handwritten_test.csv`). Raw external datasets documented below provide the foundational baselines for binary spam filtering, domain legitimacy, and URL threat detection.

---

## 1. UCI SMS Spam Collection

- **Dataset Name**: SMS Spam Collection
- **Source Link**: [https://archive.ics.uci.edu/dataset/228/sms+spam+collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- **License / Terms**: Creative Commons Attribution 4.0 International (CC BY 4.0). Free for research and educational use. Citation: Almeida, T.A., Hidalgo, J.M.G., Yamakami, A. *Contributions to the Study of SMS Spam Filtering: New Collection and Results*, ACM DOCEng'11.
- **Date Downloaded**: 2026-10-03
- **Row Count**: 5,574 rows (4,827 ham messages, 747 spam messages)
- **Storage Location**: `ml/data/raw/sms/SMSSpamCollection`
- **Format**: Tab-separated text file (`<label>\t<message>`)
- **Usage in ScamShield**: Provides binary classification baseline (ham vs spam) for text messages. Used for training and benchmarking baseline NLP models (TF-IDF + Naive Bayes / Logistic Regression / XGBoost).

---

## 2. Tranco List

- **Dataset Name**: Tranco: A Research-Oriented Top Sites Ranking
- **Source Link**: [https://tranco-list.eu/](https://tranco-list.eu/)
- **License / Terms**: Open research data / CC0. Citation: Pochat, V., van Goethem, T., Tajalizadeh, S., Joosen, W. *Tranco: A Research-Oriented Top Sites Ranking Hardened against Manipulation*, NDSS 2019.
- **Date Downloaded**: 2026-10-03
- **Row Count**: 1,000,000 domains
- **Storage Location**: `ml/data/raw/tranco/top-1m.csv`
- **Format**: CSV (`rank,domain`)
- **Usage in ScamShield**: Serves as the ground truth benign (safe) domain reference. Used by the URL analysis pipeline to verify established, high-reputation domains, identify domain spoofing/typosquatting, and calibrate lexical URL threat scoring against legitimate web traffic.

---

## 3. OpenPhish Community Feed

- **Dataset Name**: OpenPhish Community Phishing Feed
- **Source Link**: [https://openphish.com/](https://openphish.com/)
- **License / Terms**: OpenPhish Community Terms of Use. Free for non-commercial, personal, and research purposes.
- **Date Downloaded**: 2026-10-02, 2026-10-03
- **Row Count**: 300 active phishing URLs per snapshot (600 URLs total across snapshots)
- **Storage Location**:
  - `ml/data/raw/openphish/feed_20261002.txt`
  - `ml/data/raw/openphish/feed_20261003.txt`
- **Format**: Plain text file containing one active phishing URL per line
- **Usage in ScamShield**: Provides fresh, real-time malicious phishing URLs for testing URL lexical feature extraction (subdomain depth, brand spoofing, entropy, suspicious TLDs, IP hosting) and URL threat matching.
- **Safety Precaution**: Raw phishing URLs are analyzed strictly in data pipelines and must never be opened or clicked in a browser.

---

## 4. URLhaus Recent URLs

- **Dataset Name**: URLhaus Malware URL Database
- **Source Link**: [https://urlhaus.abuse.ch/downloads/csv_recent/](https://urlhaus.abuse.ch/downloads/csv_recent/)
- **License / Terms**: Creative Commons CC0 1.0 Universal (Public Domain Dedication). Powered by abuse.ch.
- **Date Downloaded**: 2026-10-03
- **Row Count**: ~15,904 active malicious URLs (excluding metadata and comment headers)
- **Storage Location**: `ml/data/raw/urlhaus/csv_recent.csv`
- **Format**: CSV (`id,dateadded,url,url_status,last_online,threat,tags,urlhaus_link,reporter`)
- **Usage in ScamShield**: High-volume verified malicious URLs used to train and validate URL security classifiers, identifying payload delivery links, suspicious host structures, and scam infrastructure.
- **Safety Precaution**: Malicious URLs are intelligence feeds; do not visit or trigger downloads directly.

---

## Data Integrity and Safety

- Phishing and malware URLs are treated as threat data only and never opened in a browser.
- Raw datasets are kept outside Git tracking via `.gitignore`.
- API keys, personal records, and credentials are never stored in the repository.

---

## Summary of Raw Datasets

| Dataset | Provider | Size / Rows | Primary Purpose | License |
|---|---|---|---|---|
| SMS Spam Collection | UCI / Almeida et al. | 5,574 messages | Binary SMS spam detection | CC BY 4.0 |
| Tranco List | Tranco-list.eu | 1,000,000 domains | Benign domain baseline | Open Research Data |
| OpenPhish Feed | OpenPhish | 300+ URLs/snapshot | Phishing URL feature detection | OpenPhish Free Community |
| URLhaus | abuse.ch | 15,000+ URLs | Malicious URL ground truth | CC0 1.0 |
