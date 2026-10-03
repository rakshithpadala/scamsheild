# ScamShield Demo Inputs

This document defines the 10 standard test inputs used for live demonstration, automated pipeline testing, and evaluation of ScamShield AI.

---

### 1. KYC / Bank-Block SMS with Link
```text
Dear Customer, your SBI YONO NetBanking account has been suspended due to pending KYC verification. Click http://sbi-kyc-update.example.xyz/pan to update your PAN immediately to avoid permanent deactivation.
```
- **Type**: SMS / Text
- **Expected Label**: Scam (Category: `bank_kyc_account`)
- **Key Indicators**: Urgent tone, fear trigger (account blockage), unofficial third-party link.

---

### 2. UPI Refund "Enter PIN" Message
```text
PhonePe Refund Alert: Your refund request of Rs 2,499 for failed merchant payment has been approved. Open Google Pay, accept the incoming collect request, and enter your 6-digit secret UPI PIN to claim funds directly into your bank.
```
- **Type**: Chat / SMS
- **Expected Label**: Scam (Category: `upi_payment`)
- **Key Indicators**: "Enter PIN to receive/claim refund" — violation of the fundamental UPI rule (PIN is debit-only).

---

### 3. Fake Job Offer with Fee
```text
Amazon HR Team: Part-time remote work opportunity for students and homemakers. Earn Rs 3,500 daily by simply rating products and reviewing hotels. To activate employee portal, deposit one-time refundable uniform & ID kit fee of Rs 1,450 to recruiter account.
```
- **Type**: WhatsApp / Messaging
- **Expected Label**: Scam (Category: `job`)
- **Key Indicators**: Unrealistic pay for trivial tasks, upfront advance payment / registration fee required.

---

### 4. Parcel / Customs-Fee Message
```text
IndiaPost Alert: Consignment IND938201 could not be dispatched due to incorrect delivery pincode. Reschedule delivery slot and pay redelivery stamp fee of Rs 48 online at http://indiapost-parcel-update.example.xyz within 24 hours.
```
- **Type**: SMS / Tracking alert
- **Expected Label**: Scam (Category: `delivery`)
- **Key Indicators**: Small fake fee lure (Rs 48) designed to harvest card details, spoofed postal domain.

---

### 5. Normal Friend Message (Benign Negative Control)
```text
Hey bro, are we still meeting at CCD at 5 PM for discussing the project presentation? Let me know if you are free.
```
- **Type**: Personal Chat
- **Expected Label**: Benign (Category: `benign`)
- **Key Indicators**: Natural informal conversation, zero urgency, no financial request, no credential harvesting.

---

### 6. Known Phishing URL from OpenPhish Feed
```text
https://facebook-logiin.vercel.app/
```
- **Type**: Malicious URL (Threat Feed)
- **Source**: OpenPhish Community Feed (`ml/data/raw/openphish/feed_20261003.txt`)
- **Expected Verdict**: `KNOWN` (Blacklisted / Malicious Phishing)
- **Safety Warning**: Raw threat intelligence data. Never open or navigate to this URL in a browser.

---

### 7. Made-Up Suspicious URL (Lexical Threat Heuristics)
```text
http://secure-login-verify.customer-auth-protection.bank-portal.example.xyz/account/ebanking/auth-step1?session=token948102
```
- **Type**: Suspicious URL (Feature-based classifier)
- **Expected Verdict**: `SUSPICIOUS`
- **Key Indicators**: Multiple subdomains (excessive depth), suspicious TLD (`.xyz`), keyword stuffing (`secure`, `login`, `verify`, `bank-portal`, `auth`), insecure HTTP protocol.

---

### 8. Benign Reference URL
```text
https://example.com
```
- **Type**: Safe / Reference URL
- **Expected Verdict**: `SAFE` / `INSUFFICIENT`
- **Key Indicators**: Official RFC 2606 reserved domain, zero lexical threat indicators, clean reputation.

---

### 9. Demo Screenshot File
```text
screenshot_01_kyc_sms_light.png
```
- **Type**: Screenshot / Image OCR
- **Storage Location**: `ml/data/demo_screenshots/screenshot_01_kyc_sms_light.png`
- **Content**: Light-mode Android SMS bubble displaying SBI KYC deactivation alert with embedded phishing link.
- **Expected Pipeline**: Tesseract OCR text extraction -> NLP Threat Classification -> URL safety scanner.

---

### 10. Copilot Knowledge Retrieval Question
```text
Is entering my UPI PIN necessary to receive money?
```
- **Type**: RAG Assistant Query
- **Expected Answer**: Clear and emphatic "NO". A UPI PIN is solely required to send or debit money from your account, never to receive money or cashback.
- **Expected Citation**: NPCI UPI Safety Guidelines ([`knowledge_base/raw/npci_upi_safety_guide.pdf`](file:///c:/Users/Nice/ScamSheild/knowledge_base/raw/npci_upi_safety_guide.pdf)).
