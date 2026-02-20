import logging

from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import Topic


logger = logging.getLogger(__name__)


def test_topic() -> None:
    client = TestClient(app)
    new_topic = Topic(name="NewTopic", description="This is a description")
    logger.info("Creating topic: %s", new_topic.name)
    response = client.post(
        "/api/v1/topic",
        json=new_topic.model_dump(),
    )
    logger.info("Create topic response status=%s body=%s", response.status_code, response.text)

    response = response.json()
    assert response["name"] == new_topic.name
    assert response["description"] == new_topic.description


def test_topic_409() -> None:
    client = TestClient(app)
    new_topic = Topic(name="ConflictTopic", description="Conflict topic description")

    first_response = client.post(
        "/api/v1/topic",
        json=new_topic.model_dump(),
    )
    logger.info(
        "First create topic response status=%s body=%s",
        first_response.status_code,
        first_response.text,
    )

    second_response = client.post(
        "/api/v1/topic",
        json=new_topic.model_dump(),
    )
    logger.info(
        "Second create topic response status=%s body=%s",
        second_response.status_code,
        second_response.text,
    )

    assert second_response.status_code == 409
    res = second_response.json()
    assert "already exists" in res["detail"]
