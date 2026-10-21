import pytest
from fastapi.testclient import TestClient
import sys
import os
import io

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app

client = TestClient(app)


def test_chat_message():
    payload = {
        "message": "What are the symptoms and treatment of Banana Black Sigatoka?",
        "crop": "Banana",
        "condition": "Black Sigatoka"
    }
    response = client.post("/api/v1/chat/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "Sigatoka" in data["response"] or "Banana" in data["response"]
    assert "session_id" in data
    assert len(data["sources"]) > 0

    # Test history retrieval
    session_id = data["session_id"]
    hist_resp = client.get(f"/api/v1/chat/history/{session_id}")
    assert hist_resp.status_code == 200
    hist_data = hist_resp.json()
    assert len(hist_data["messages"]) >= 2  # user + assistant


def test_chat_telugu_support():
    payload = {
        "message": "వరిలో అగ్గితెగులు లక్షణాలు మరియు నివారణ ఏమిటి?",
        "crop": "Rice",
        "condition": "Blast",
        "language": "te"
    }
    response = client.post("/api/v1/chat/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    # Verify Telugu response contains localized headings
    assert "రైతు" in data["response"] or "వరి" in data["response"]


def test_chat_missing_context_safety():
    # Chemical spray query without crop or growth stage
    payload = {
        "message": "What is the immediate chemical spray and dosage per acre?",
    }
    response = client.post("/api/v1/chat/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Should flag missing context
    assert "Context" in data["response"] or "Safety" in data["response"]


def test_agent_diagnose():
    payload = {
        "image_result": {
            "crop": "Banana",
            "condition": "Black Sigatoka",
            "category": "Disease",
            "confidence": 0.88
        },
        "farmer_question": "What immediate chemical spray should I use?"
    }
    response = client.post("/api/v1/agent/diagnose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["crop"] == "Banana"
    assert data["urgency_level"] in ["High", "Moderate", "Low"]
    assert "final_answer" in data
    assert len(data["action_plan"]) > 0


def test_history_stats():
    response = client.get("/api/v1/history/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_predictions"] >= 0
    assert data["active_models"] > 0
    assert data["covered_districts"] > 0


def test_disease_detection_upload():
    # Create synthetic test image in memory
    from PIL import Image
    img = Image.new("RGB", (200, 200), color=(73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    response = client.post(
        "/api/v1/detect/disease",
        files={"file": ("test_leaf.jpg", img_byte_arr, "image/jpeg")},
        data={"target_crop": "Banana"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "crop" in data
    assert "category" in data
    assert "suggested_actions" in data
