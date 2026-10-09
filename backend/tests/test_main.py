"""Unit tests for ScamShield Backend API."""
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import InputType, Verdict

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_analyze_upi_scam():
    payload = {
        "text": "Congratulations! You received Rs 2,500 cashback reward. Click here to approve collect request and enter UPI PIN to receive money."
    }
    response = client.post("/analyze/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == Verdict.SUSPICIOUS.value
    assert data["category"]["label"] == "upi_payment"
    assert data["risk_score"] > 80
    assert len(data["evidence"]) > 0


def test_analyze_known_phishing():
    payload = {
        "text": "Please check your account at https://facebook-logiin.vercel.app/ immediately."
    }
    response = client.post("/analyze/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == Verdict.KNOWN_THREAT.value
    assert data["risk_score"] >= 95


def test_analyze_benign_otp():
    payload = {
        "text": "482913 is your secret One Time Password (OTP) for online purchase of Rs 2,199. Valid for 10 minutes. Do not share OTP with anyone."
    }
    response = client.post("/analyze/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == Verdict.LOW_RISK.value
    assert data["category"]["label"] == "benign"
    assert data["risk_score"] <= 20


def test_analyze_insufficient():
    payload = {
        "text": "Hi"
    }
    response = client.post("/analyze/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == Verdict.INSUFFICIENT_EVIDENCE.value


def test_demo_screenshots_catalog():
    response = client.get("/api/demo-screenshots")
    assert response.status_code == 200
    demos = response.json()
    assert len(demos) == 6
    assert demos[0]["id"] == "screenshot_01"
    assert "url" in demos[0]


def test_ocr_extract_endpoint():
    sample_img = Path("ml/data/demo_screenshots/screenshot_01_kyc_sms_light.png")
    if sample_img.exists():
        with open(sample_img, "rb") as f:
            response = client.post(
                "/ocr/extract",
                files={"file": ("screenshot_01.png", f, "image/png")},
            )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "confidence" in data
        if data["confidence"] > 0:
            assert data["confidence"] > 0.5
            assert "SBI" in data["text"] or "suspended" in data["text"].lower() or "kyc" in data["text"].lower()


def test_analyze_screenshot_endpoint():
    sample_img = Path("ml/data/demo_screenshots/screenshot_02_upi_collect_dark.png")
    if sample_img.exists():
        with open(sample_img, "rb") as f:
            response = client.post(
                "/analyze/screenshot",
                files={"file": ("screenshot_02.png", f, "image/png")},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["input_type"] == InputType.SCREENSHOT.value
        assert data["ocr"] is not None
        assert "confidence" in data["ocr"]
        if data["ocr"]["confidence"] > 0:
            assert data["verdict"] == Verdict.SUSPICIOUS.value
            assert len(data["ocr"]["text"]) > 0
