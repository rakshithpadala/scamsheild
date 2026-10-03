"""Unit tests for ScamShield Backend API."""
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "provider" in data

def test_analyze_upi_scam():
    payload = {
        "text": "Congratulations! You received Rs 2,500 cashback reward. Click here to approve collect request and enter UPI PIN to receive money."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "SUSPICIOUS"
    assert data["category"] == "upi_payment"
    assert data["risk_score"] > 80
    assert len(data["highlighted_phrases"]) > 0
    assert len(data["stages"]) == 6

def test_analyze_known_phishing():
    payload = {
        "text": "Please check your account at https://facebook-logiin.vercel.app/ immediately."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "KNOWN"
    assert data["risk_score"] >= 95

def test_analyze_benign_otp():
    payload = {
        "text": "482913 is your secret One Time Password (OTP) for online purchase of Rs 2,199. Valid for 10 minutes. Do not share OTP with anyone."
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "SAFE"
    assert data["category"] == "benign"
    assert data["risk_score"] < 20

def test_analyze_insufficient():
    payload = {
        "text": "Hi"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "INSUFFICIENT"
