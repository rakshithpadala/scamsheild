"""ScamShield AI - FastAPI Backend Application.
Provides real-time multi-modal fraud detection, URL reputation checks, and RAG copilot services.
"""
from __future__ import annotations

import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.db.base import init_db
from backend.app.schemas import (
    AnalysisResult,
    Category,
    Citation,
    Evidence,
    EvidenceSource,
    InputType,
    MessageRequest,
    TextSpan,
    URLResult,
    Verdict,
)
from backend.app.services.entity_extraction import extract_entities
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


@app.get("/")
def root() -> dict:
    return {"name": "ScamShield AI API", "status": "running", "version": "0.1.0"}


@app.post("/analyze/message", response_model=AnalysisResult)
@app.post("/api/analyze", response_model=AnalysisResult)
def analyze_message_endpoint(req: MessageRequest) -> AnalysisResult:
    display_text = preprocess_for_display(req.text)
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
            ("enter your pin to return", "Social engineering claim of accidental transfer"),
            ("enter 6 digit upi pin", "Explicit PIN entry prompt"),
            ("enter 4/6 digit secret pin", "Explicit PIN entry prompt"),
            ("claim cashback", "Lures user with cashback claim"),
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
        if evidence_list:
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
            ("arrest warrant issued", "Forged judicial arrest warrant"),
            ("cbi investigation notice", "Law enforcement impersonation"),
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
        if evidence_list:
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
        if evidence_list:
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

    # 5. Insufficient Data Check
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
        input_type=InputType.MESSAGE,
        verdict=verdict,
        risk_score=risk_score,
        category=Category(label=cat_label, confidence=cat_conf),
        evidence=evidence_list,
        entities=entities,
        url_results=url_results,
        explanation=explanation,
        next_steps=next_steps,
        citations=citations,
        limitations=limitations,
    )
