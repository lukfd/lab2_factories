from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_classify_with_nearest_strategy() -> None:
    response = client.post(
        "/api/v1/emails",
        json={
            "subject": "Budget planning seed",
            "body": "Please review the quarterly budget",
            "topic": "work",
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/emails/classify",
        json={
            "subject": "Budget review meeting",
            "body": "Please check the quarterly budget and plans",
            "strategy": "nearest",
        },
    )

    assert response.status_code == 200
    response = response.json()
    assert isinstance(response["predicted_topic"], str)
    assert isinstance(response["topic_scores"], dict)
    assert response["predicted_topic"] in response["available_topics"]
