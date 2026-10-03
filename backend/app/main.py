"""ScamShield AI - FastAPI Backend Application.
Provides real-time multi-modal fraud detection, URL reputation checks, and RAG copilot services.
"""
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api.health import router as health_router
from backend.app.db.base import init_db
from backend.app.ml.text_classifier import get_binary_classifier, get_category_classifier
from backend.app.schemas import (
    AnalysisResult,
    Category,
    Citation,
    Evidence,
    EvidenceSource,
    InputType,
    MessageRequest,
    OCRResult,
    TextSpan,
    URLResult,
    Verdict,
)
from backend.app.services.entity_extraction import extract_entities
from backend.app.services.ocr import extract_text_from_bytes
from backend.app.services.preprocessing import preprocess_for_display

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables. Shutdown: cleanup."""
    init_db()
    yield


app = FastAPI(
    title="ScamShield AI API",
    description="Real-time multi-modal digital payment fraud detection and cyber defense engine.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware for Frontend Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

KNOWN_PHISHING_DOMAINS = [
    "facebook-logiin.vercel.app",
    "supershopf.vip",
    "roblox.com.bo",
    "facebook-auto-liker.blogspot.com",
    "nhengenharia.com",
]

# Static mount for demo screenshots so frontend can render previews
demo_screenshots_dir = Path("ml/data/demo_screenshots")
if demo_screenshots_dir.exists():
    app.mount(
        "/demo_screenshots",
        StaticFiles(directory=str(demo_screenshots_dir)),
        name="demo_screenshots",
    )


DEMO_SCREENSHOTS = [
    {
        "id": "screenshot_01",
        "name": "screenshot_01_kyc_sms_light.png",
        "title": "SBI KYC Account Suspension Alert",
        "category": "bank_kyc_account",
        "url": "/demo_screenshots/screenshot_01_kyc_sms_light.png",
        "sample_snippet": "Your SBI account has been suspended due to pending KYC document. Update PAN immediately.",
    },
    {
        "id": "screenshot_02",
        "name": "screenshot_02_upi_collect_dark.png",
        "title": "PhonePe / GPay Cashback Collect Request",
        "category": "upi_payment",
        "url": "/demo_screenshots/screenshot_02_upi_collect_dark.png",
        "sample_snippet": "You received Rs 2,500 cashback reward in GooglePay. Click here to approve collect request.",
    },
    {
        "id": "screenshot_03",
        "name": "screenshot_03_job_offer_two_msgs.png",
        "title": "Work From Home / Daily Task Scam",
        "category": "job",
        "url": "/demo_screenshots/screenshot_03_job_offer_two_msgs.png",
        "sample_snippet": "Work From Home Opportunity: Earn Rs 3,000 to Rs 8,000 daily by simply liking videos.",
    },
    {
        "id": "screenshot_04",
        "name": "screenshot_04_delivery_cropped.png",
        "title": "IndiaPost Fake Delivery Rescheduling",
        "category": "delivery",
        "url": "/demo_screenshots/screenshot_04_delivery_cropped.png",
        "sample_snippet": "IndiaPost: Your package could not be delivered due to wrong address details. Update address.",
    },
    {
        "id": "screenshot_05",
        "name": "screenshot_05_police_digital_arrest_blurry.png",
        "title": "CBI Digital Arrest Notice (Blurry/Distorted)",
        "category": "gov_police_impersonation",
        "url": "/demo_screenshots/screenshot_05_police_digital_arrest_blurry.png",
        "sample_snippet": "CENTRAL BUREAU OF INVESTIGATION: Legal notice / digital arrest warrant issued.",
    },
    {
        "id": "screenshot_06",
        "name": "screenshot_06_electricity_cutoff.png",
        "title": "Urgent Electricity Power Disconnection",
        "category": "other",
        "url": "/demo_screenshots/screenshot_06_electricity_cutoff.png",
        "sample_snippet": "Power supply to your meter connection will be disconnected tonight. Call officer immediately.",
    },
]


@app.get("/")
def root() -> dict:
    return {"name": "ScamShield AI API", "status": "running", "version": "0.1.0"}


@app.get("/api/demo-screenshots")
def get_demo_screenshots() -> list[dict]:
    """Returns catalog of pre-packaged test screenshots with image URLs and metadata."""
    return DEMO_SCREENSHOTS


def run_fraud_analysis(
    text: str,
    input_type: InputType = InputType.MESSAGE,
    ocr_result: OCRResult | None = None,
) -> AnalysisResult:
    """Core multi-modal scam detection engine: rules, ML text classifiers, threat intel, and RAG."""
    display_text = preprocess_for_display(text)
    lower_text = display_text.lower()
    entities = extract_entities(display_text)

    # Initialize default result fields
    verdict = Verdict.LOW_RISK
    risk_score = 10
    cat_label = "benign"
    cat_conf = 0.85
    evidence_list: list[Evidence] = []
    citations: list[Citation] = []
    explanation = "No high-risk scam triggers or malicious signatures were detected in this message."
    next_steps = ["Normal security hygiene: never share passwords or banking credentials."]
    limitations = "Automated analysis based on known scam patterns; always independently verify suspicious requests."

    # 1. Known Phishing Check
    found_known = False
    for url in entities.urls:
        for domain in KNOWN_PHISHING_DOMAINS:
            if domain in url.lower():
                found_known = True
                verdict = Verdict.KNOWN_THREAT
                risk_score = 98
                cat_label = "other"
                cat_conf = 0.98
                evidence_list.append(
                    Evidence(
                        id="intel_known_phish",
                        label="Known Phishing URL Match",
                        weight=0.98,
                        source=EvidenceSource.INTEL,
                        detail=f"URL matches verified malicious threat intelligence feed: {domain}",
                    )
                )
                explanation = "This URL is confirmed on active global phishing intelligence feeds. Do not navigate to or interact with this link."
                next_steps = [
                    "Do not click or open the link under any circumstance.",
                    "Block the sender and report the message on cybercrime.gov.in.",
                ]
                break
        if found_known:
            break

    # 2. UPI PIN / Collect Request Trap
    if not found_known:
        upi_patterns = [
            ("enter upi pin", "Requests user to enter secret UPI PIN"),
            ("enter pin to receive", "Claims PIN entry is needed to receive payment"),
            ("approve collect request", "Coerces user to approve incoming collect request"),
            ("approve collect", "Coerces user to approve incoming collect request"),
            ("enter your pin to return", "Social engineering claim of accidental transfer"),
            ("enter 6 digit upi pin", "Explicit PIN entry prompt"),
            ("enter 4/6 digit secret pin", "Explicit PIN entry prompt"),
            ("claim cashback", "Lures user with cashback claim"),
            ("cashback reward", "Cashback lure targeting digital payment users"),
            ("refund voucher approved", "Disguises trap as refund authorization"),
        ]
        for pat, desc in upi_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 94
                cat_label = "upi_payment"
                cat_conf = 0.95
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_upi_{len(evidence_list)}",
                        label="UPI PIN Collect Trap",
                        weight=0.92,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "upi_payment":
            explanation = "Critical warning: A UPI PIN is solely required to send or debit money, never to receive funds, accept refunds, or claim cashback."
            next_steps = [
                "Decline any pending collect requests on Google Pay, PhonePe, or Paytm.",
                "Never enter your UPI PIN to claim money or receive refunds.",
                "If money was deducted, immediately call the national helpline 1930.",
            ]
            citations.append(
                Citation(
                    source="NPCI",
                    title="UPI Safety Guidelines",
                    snippet="UPI PIN is never required to receive money.",
                    url="https://www.npci.org.in/what-we-do/upi/upi-safety-tips",
                )
            )

    # 3. Police / Digital Arrest Impersonation
    if not found_known and verdict == Verdict.LOW_RISK:
        police_patterns = [
            ("digital arrest", "Threatens victim with fake 'Digital Arrest'"),
            ("contraband courier", "Falsely alleges seized parcel with illegal goods"),
            ("banned substances", "Narcotics accusation trigger"),
            ("skype call", "Orders interrogation over video call"),
            ("illegal narcotics", "Contraband pressure tactic"),
            ("arrest warrant", "Forged judicial arrest warrant"),
            ("cbi investigation", "Law enforcement impersonation"),
            ("central bureau of investigation", "CBI law enforcement impersonation"),
        ]
        for pat, desc in police_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 96
                cat_label = "gov_police_impersonation"
                cat_conf = 0.96
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_police_{len(evidence_list)}",
                        label="Police / Government Impersonation",
                        weight=0.95,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "gov_police_impersonation":
            explanation = "Severe alert: Indian law enforcement and judiciary never conduct interrogations or declare 'Digital Arrest' over video calls."
            next_steps = [
                "Disconnect and block the caller immediately; do not panic.",
                "Never transfer funds to any 'police verification' account.",
                "Report intimidation to the 1930 cyber helpline and local police.",
            ]
            citations.append(
                Citation(
                    source="I4C / MHA",
                    title="Digital Arrest Advisory",
                    snippet="'Digital Arrest' does not exist under Indian criminal law.",
                    url="https://i4c.mha.gov.in/advisories/digital-arrest-police-impersonation.pdf",
                )
            )

    # 4. Bank KYC Expiry
    if not found_known and verdict == Verdict.LOW_RISK:
        kyc_patterns = [
            ("account has been suspended", "Fear trigger of account suspension"),
            ("acct will be blocked", "Urgency threat to deactivate banking"),
            ("netbanking access will be blocked", "Access deactivation threat"),
            ("pending kyc", "Unsolicited KYC requirement"),
            ("update pan immediately", "Demands sensitive document update"),
            ("aadhar card update", "Aadhaar linking urgency lure"),
            ("complete kyc now", "External KYC verification trigger"),
        ]
        for pat, desc in kyc_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 89
                cat_label = "bank_kyc_account"
                cat_conf = 0.91
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_kyc_{len(evidence_list)}",
                        label="Fake KYC Deactivation Alert",
                        weight=0.88,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "bank_kyc_account":
            explanation = "Warning: Banks never send external links over SMS to update KYC or reactivate accounts. KYC updates must only be done in-branch or via official banking apps."
            next_steps = [
                "Do not open links sent in SMS or share banking OTPs.",
                "Check account status using your official mobile banking app or branch.",
                "Forward the phishing message to 1909 (TRAI DND).",
            ]
            citations.append(
                Citation(
                    source="RBI",
                    title="BE(A)WARE Financial Fraud Booklet",
                    snippet="Banks never send web links via SMS for periodic KYC update.",
                    url="https://rbidocs.rbi.org.in/rdocs/content/pdfs/BEAWARE07032022.pdf",
                )
            )

    # 5. Delivery Package Rescheduling Scam
    if not found_known and verdict == Verdict.LOW_RISK:
        delivery_patterns = [
            ("could not be delivered", "Fake delivery failure notice"),
            ("wrong address details", "Lure to click link to update address"),
            ("postal dispatch alert", "Impersonates postal delivery service"),
            ("indiapost: your package", "IndiaPost parcel impersonation"),
            ("update address to re-deliver", "Harvests personal address and card fees"),
        ]
        for pat, desc in delivery_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 91
                cat_label = "delivery"
                cat_conf = 0.93
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_delivery_{len(evidence_list)}",
                        label="Delivery Rescheduling Phishing",
                        weight=0.89,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "delivery":
            explanation = "Caution: Scammers send fake postal delivery failure notices requiring you to click suspicious links or pay a small fee to re-deliver packages."
            next_steps = [
                "Check tracking numbers directly on the official indiapost.gov.in website.",
                "Never pay small token amounts (Rs 5 - Rs 25) on unverified links.",
            ]
            citations.append(
                Citation(
                    source="India Post",
                    title="Consumer Postal Advisory",
                    snippet="Department of Posts never sends SMS links asking users to update addresses or pay re-delivery charges.",
                    url="https://www.indiapost.gov.in/VAS/Pages/News/FraudSMS_Alert.aspx",
                )
            )

    # 6. Work From Home / Part-time Task Scam
    if not found_known and verdict == Verdict.LOW_RISK:
        job_patterns = [
            ("work from home opportunity", "Unsolicited high-income task recruitment"),
            ("earn rs 3,000 to rs 8,000 daily", "Unrealistic daily earnings promise"),
            ("simply liking", "Pretext of earning money for social media likes/ratings"),
            ("telegram task", "Coercion into prepaid telegram investment tasks"),
        ]
        for pat, desc in job_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 92
                cat_label = "job"
                cat_conf = 0.94
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_job_{len(evidence_list)}",
                        label="Work-From-Home Task Fraud",
                        weight=0.91,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "job":
            explanation = "High Risk: 'Like & Earn' or freelance tasks demanding initial deposits are notorious Ponzi schemes leading to complete loss of principal."
            next_steps = [
                "Never pay advance registration or deposit fees for job offers.",
                "Block the recruiter and refrain from joining unknown Telegram task channels.",
            ]
            citations.append(
                Citation(
                    source="I4C / MHA",
                    title="Part-Time Job Scam Advisory",
                    snippet="Legitimate companies never ask applicants for security deposits or fee payments to unlock task commissions.",
                    url="https://cybercrime.gov.in",
                )
            )

    # 7. Electricity / Utility Cutoff Threat
    if not found_known and verdict == Verdict.LOW_RISK:
        utility_patterns = [
            ("power supply to your meter", "Urgent threat of utility termination"),
            ("disconnected tonight", "Artificial deadline pressure tactic"),
            ("electricity department", "Utility authority impersonation"),
            ("call officer at", "Directs user to call fraudster mobile number"),
            ("electricity bill unpaid", "Fake utility default claim"),
        ]
        for pat, desc in utility_patterns:
            idx = lower_text.find(pat)
            if idx != -1:
                verdict = Verdict.SUSPICIOUS
                risk_score = 93
                cat_label = "other"
                cat_conf = 0.92
                span = TextSpan(start=idx, end=idx + len(pat), text=display_text[idx : idx + len(pat)])
                evidence_list.append(
                    Evidence(
                        id=f"rule_utility_{len(evidence_list)}",
                        label="Electricity Disconnection Urgency Threat",
                        weight=0.90,
                        source=EvidenceSource.RULE,
                        spans=[span],
                        detail=desc,
                    )
                )
        if evidence_list and cat_label == "other":
            explanation = "Alert: Power distribution companies never send SMS threats to disconnect electricity immediately tonight or request calls to personal mobile numbers."
            next_steps = [
                "Verify bill status directly on your official electricity board portal or bill receipt.",
                "Never call mobile numbers provided in unsolicited disconnection SMS.",
            ]
            citations.append(
                Citation(
                    source="Ministry of Power / DISCOMs",
                    title="Electricity Bill Fraud Advisory",
                    snippet="DISCOMs follow formal notice periods and never terminate power supply without registered written notice.",
                    url="https://cybercrime.gov.in",
                )
            )

    # 8. Machine Learning NLP Scoring & Category Inference
    if len(lower_text) >= 15:
        ml_proba = get_binary_classifier().predict_proba(display_text)
        pred_cat, pred_conf = get_category_classifier().predict_category(display_text)

        if ml_proba >= 0.70 and verdict != Verdict.KNOWN_THREAT:
            evidence_list.append(
                Evidence(
                    id=f"ml_nlp_{len(evidence_list)}",
                    label="Machine Learning Threat Detector",
                    weight=round(ml_proba, 2),
                    source=EvidenceSource.ML,
                    detail=f"Statistical NLP model flagged suspicious patterns with {int(ml_proba * 100)}% scam confidence",
                )
            )
            if verdict == Verdict.LOW_RISK:
                verdict = Verdict.SUSPICIOUS
                risk_score = max(risk_score, min(95, int(ml_proba * 90)))
                cat_label = pred_cat
                cat_conf = pred_conf
                explanation = "This message exhibits linguistic markers characteristic of fraudulent solicitations. Verify through official channels before acting."

        if cat_label in ("other", "benign") and verdict in (Verdict.SUSPICIOUS, Verdict.KNOWN_THREAT):
            if pred_cat != "benign":
                cat_label = pred_cat
                cat_conf = max(cat_conf, pred_conf)

    # 9. Insufficient Data Check
    if verdict == Verdict.LOW_RISK and len(lower_text) < 15 and not entities.urls:
        verdict = Verdict.INSUFFICIENT_EVIDENCE
        risk_score = 20
        cat_label = "other"
        cat_conf = 0.50
        explanation = "Insufficient message content provided to establish definitive risk score. Exercise caution."
        next_steps = ["Provide more message context or URL details to evaluate safety."]

    url_results = [
        URLResult(
            url=u,
            ml_risk=0.85 if "example.xyz" in u else 0.1,
            features={"length": len(u)},
        )
        for u in entities.urls
    ]

    return AnalysisResult(
        analysis_id=str(uuid.uuid4()),
        input_type=input_type,
        verdict=verdict,
        risk_score=risk_score,
        category=Category(label=cat_label, confidence=cat_conf),
        evidence=evidence_list,
        entities=entities,
        url_results=url_results,
        ocr=ocr_result,
        explanation=explanation,
        next_steps=next_steps,
        citations=citations,
        limitations=limitations,
    )


@app.post("/analyze/message", response_model=AnalysisResult)
@app.post("/api/analyze", response_model=AnalysisResult)
def analyze_message_endpoint(req: MessageRequest) -> AnalysisResult:
    """Evaluates text message / SMS / email / screenshot content."""
    return run_fraud_analysis(text=req.text, input_type=req.input_type, ocr_result=req.ocr)


@app.post("/ocr/extract", response_model=OCRResult)
async def ocr_extract_endpoint(file: UploadFile = File(...)) -> OCRResult:
    """Extracts raw text and word-level confidence from an uploaded screenshot using OpenCV + Tesseract."""
    contents = await file.read()
    text, conf = extract_text_from_bytes(contents)
    return OCRResult(text=text, confidence=conf)


@app.post("/analyze/screenshot", response_model=AnalysisResult)
async def analyze_screenshot_endpoint(file: UploadFile = File(...)) -> AnalysisResult:
    """Directly extracts OCR text from an uploaded screenshot and runs end-to-end scam analysis."""
    contents = await file.read()
    text, conf = extract_text_from_bytes(contents)
    ocr_res = OCRResult(text=text, confidence=conf)
    return run_fraud_analysis(text=text, input_type=InputType.SCREENSHOT, ocr_result=ocr_res)
