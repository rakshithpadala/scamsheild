# ScamShield AI — 3-Minute Live Demo & Video Recording Script (Task T17)
*Step-by-step walkthrough for recording `docs/demo.mp4` or presenting live during the viva examination.*

---

## Recording Guidelines
- **Target Duration**: 2 minutes 30 seconds to 3 minutes max.
- **Recording Tool**: OBS Studio or Windows Game Bar (`Win + Alt + R`).
- **Resolution**: 1080p (1920×1080), browser at 100% zoom.
- **Preparation**:
  1. Terminal 1: Run backend API (`uvicorn backend.app.main:app --port 8000`) or Docker Compose (`docker compose up --build`).
  2. Terminal 2: Run frontend dev server (`cd frontend && npm run dev`).
  3. Terminal 3: Run MLflow UI (`.\.venv\Scripts\python.exe -m mlflow ui`).
  4. Browser Tab 1: Frontend at `http://localhost:5173`.
  5. Browser Tab 2: MLflow UI at `http://localhost:5000`.

---

## ⏱️ Scene-by-Scene Script & Action Timeline

### Scene 1: Problem Hook & Introduction (0:00 – 0:25)
- **Visual**: Home page of ScamShield AI showing the dark security command-center with the 4 tabs (Message, Screenshot, URL, Email).
- **Spoken Voiceover**:
  > *"Every day, thousands of Indian citizens lose their hard-earned money to deceptive UPI collect requests, fake KYC expiry warnings, and forged digital arrest threats. Existing spam filters simply flag 'spam' without explaining the deception mechanism or citing official guidance. ScamShield AI is a multi-modal digital safety assistant designed to Detect, Investigate, Explain, Verify, and Act Safely."*

---

### Scene 2: Text Message Scan — The UPI PIN Trap (0:25 – 1:05)
- **Action**:
  1. Click the **Text Message** tab.
  2. Paste **Demo Input #2** from `docs/demo_inputs.md`:
     ```text
     PhonePe Refund Alert: Your refund request of Rs 2,499 for failed merchant payment has been approved. Open Google Pay, accept the incoming collect request, and enter your 6-digit secret UPI PIN to claim funds directly into your bank.
     ```
  3. Click **"Analyze Message"**.
- **Visual Highlights**:
  - Point mouse to the animated **Risk Gauge** showing `SUSPICIOUS` (Score 94).
  - Point to the **Category Badge**: `upi_payment` with high confidence.
  - Show the **Original Text with Highlighted Text Spans**: *"enter your 6-digit secret UPI PIN"*.
  - Show the **Evidence Progress Bars**: Rule Engine (0.92 weight) + Statistical NLP Threat Detector (0.85 weight).
  - Point to the **Official NPCI Citation**: *"UPI PIN is never required to receive money."*
- **Spoken Voiceover**:
  > *"Notice how ScamShield doesn't just guess a score. It breaks down the exact deception: the fraudster is coercing the user to approve a collect request and enter their UPI PIN under the guise of receiving a refund. ScamShield highlights the exact text span, calculates evidence from both deterministic rules and our statistical NLP classifier, and cites official NPCI safety guidelines. If money was already deducted, it immediately provides the 1930 national cyber helpline."*

---

### Scene 3: Known Threat Intel URL Scanner (1:05 – 1:40)
- **Action**:
  1. Click the **URL Scanner** tab.
  2. Enter **Demo Input #6**:
     ```text
     https://facebook-logiin.vercel.app/
     ```
  3. Click **"Check URL Safety"**.
- **Visual Highlights**:
  - Show the red **KNOWN_THREAT** badge and risk score of **98**.
  - Show the **Threat Intel Feed Pill**: `Matched Active OpenPhish Feed`.
  - Highlight the SSRF-safe warning: *"Do not open or interact with this link."*
- **Spoken Voiceover**:
  > *"Next, we evaluate an external URL. Unlike tools that blindly execute external links on the server, ScamShield is completely SSRF-safe. It performs offline lexical inspection and cross-references active global threat intelligence feeds like OpenPhish and URLhaus. Because this domain is a verified active phishing site, our fusion engine triggers an immediate override to KNOWN_THREAT."*

---

### Scene 4: Device Screenshot OCR Extraction (1:40 – 2:15)
- **Action**:
  1. Click the **Screenshot Scanner** tab.
  2. Upload `ml/data/demo_screenshots/screenshot_05_police_digital_arrest_blurry.png`.
  3. Show the OCR extracted text with editable side-by-side view.
  4. Click **"Analyze Extracted Text"**.
- **Visual Highlights**:
  - Point to the bilateral-filtered OCR extraction capturing the fake police summons text.
  - Show Verdict: `SUSPICIOUS`, Category: `gov_police_impersonation`.
  - Point to the official **I4C / Ministry of Home Affairs Advisory Citation**: *"'Digital Arrest' does not exist under Indian criminal law."*
- **Spoken Voiceover**:
  > *"When a victim receives a coercive image on WhatsApp, our computer vision pipeline applies noise reduction and adaptive binarization before extracting text with Tesseract OCR. Here, ScamShield detects the notorious 'Digital Arrest' extortion scheme, classifies the impersonation threat, and cites the Ministry of Home Affairs advisory stating that Indian law enforcement never conducts interrogations or arrests over video calls."*

---

### Scene 5: RAG Copilot & Model Lab Transparency (2:15 – 2:45)
- **Action**:
  1. Open the **Copilot Drawer** on the right side.
  2. Ask: *"Is my UPI PIN ever needed to receive a cash prize or refund?"*
  3. Show the instant, strictly grounded response citing NPCI documentation.
  4. Switch to Browser Tab 2: Show the **MLflow Dashboard** (`http://localhost:5000`).
- **Visual Highlights**:
  - Point to the comparison table of 6 binary text models on UCI SMS Spam.
  - Show **Logistic Regression** selected for top Recall (**93.96%**) at acceptable FPR (**0.93%**).
  - Point to the 10-class category benchmark evaluated on the independent handwritten test set.
- **Spoken Voiceover**:
  > *"Our RAG Copilot answers factual digital safety questions strictly grounded in official regulatory source documents without hallucinations. And on the Model Lab dashboard tracked in MLflow, we prioritize high Recall over raw accuracy alone, ensuring false negatives are minimized. Logistic Regression achieves 93.96% Recall with sub-millisecond inference."*

---

### Scene 6: Ethics & Conclusion (2:45 – 3:00)
- **Visual**: Return to the ScamShield home screen, highlighting the zero-credential notice.
- **Spoken Voiceover**:
  > *"ScamShield AI never collects or persists user passwords, UPI PINs, or OTPs, and the LLM is never allowed to dictate verdicts. By combining statistical ML, deterministic rules, live threat intelligence, and regulatory citations, ScamShield AI delivers a transparent, responsible digital safety companion for India. Thank you."*
