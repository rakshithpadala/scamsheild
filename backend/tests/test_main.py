"""Unit tests for ScamShield Backend API."""
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import Verdict

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
