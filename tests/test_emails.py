from fastapi.testclient import TestClient
from uuid import UUID

from app.main import app


client = TestClient(app)


def test_store_email_topic() -> None:
    response = client.post(
        "/api/v1/emails",
        json={
            "subject": "Budget planning",
            "body": "Please review quarterly budget updates",
            "topic": "work",
        },
    )

    assert response.status_code == 200
    response = response.json()
    assert response["message"] == "Email stored successfully"
    assert isinstance(response["email_id"], str)


def test_store_email_without_topic() -> None:
    response = client.post(
        "/api/v1/emails",
        json={
            "subject": "Family dinner",
            "body": "Let's have dinner on Sunday",
        },
    )

    assert response.status_code == 200
    response = response.json()
    assert response["message"] == "Email stored successfully"
    assert isinstance(response["email_id"], str)
