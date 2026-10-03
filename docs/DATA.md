# ScamShield AI — Dataset Documentation

This file records the external datasets and feeds used in the ScamShield AI project.

## 1. UCI SMS Spam Collection

- **Dataset:** SMS Spam Collection
- **Source:** UCI Machine Learning Repository
- **Link:** https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- **License/Terms:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Download date:** YYYY-MM-DD
- **Local file:** `ml/data/raw/sms/SMSSpamCollection`
- **Row count:** TODO — enter the count from the downloaded file
- **Use in ScamShield:** Used as the baseline labeled dataset for SMS/text spam classification and evaluation.

## 2. Tranco Top Sites List

- **Dataset:** Tranco Top Sites List
- **Source:** Tranco
- **Link:** https://tranco-list.eu/
- **License/Terms:** See the current Tranco attribution and provider terms on the Tranco website.
- **Download date:** YYYY-MM-DD
- **Local file:** `ml/data/raw/tranco/top-1m.csv`
- **Row count:** TODO — enter the count from the downloaded file
- **Use in ScamShield:** Used as a reference set of popular/legitimate domains for URL analysis and comparison.

## 3. OpenPhish Community Feed

- **Dataset:** OpenPhish Community Phishing Feed
- **Source:** OpenPhish
- **Link:** https://openphish.com/phishing_feeds.html
- **License/Terms:** OpenPhish Community Feed — use is subject to OpenPhish Terms of Use.
- **Download date:** YYYY-MM-DD
- **Local file:** `ml/data/raw/openphish/feed_YYYYMMDD.txt`
- **Row count:** TODO — enter the number of URL records in the downloaded feed
- **Use in ScamShield:** Used as phishing-URL intelligence and for training/validation of URL analysis components where permitted by the applicable terms.

## 4. URLhaus Recent URLs

- **Dataset:** URLhaus Recent URL Database
- **Source:** URLhaus / abuse.ch
- **Link:** https://urlhaus.abuse.ch/api/
- **License/Terms:** URLhaus Community API is available free of charge under its fair-use principles; applicable terms must be followed.
- **Download date:** YYYY-MM-DD
- **Local file:** `ml/data/raw/urlhaus/csv_recent.csv`
- **Row count:** TODO — enter the number of URL records in the downloaded CSV
- **Use in ScamShield:** Used as malware-URL threat intelligence and as an additional signal in URL-risk analysis.

## Data Integrity and Safety

- Phishing and malware URLs are treated as data only.
- URLs from threat-intelligence feeds must not be opened or clicked.
- Raw datasets are kept outside Git tracking.
- API keys and authentication credentials are never stored in the repository.

## Dataset Honesty Statement

Scam categories use synthetic data plus a hand-written test set.