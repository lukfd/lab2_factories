import json
import uuid

from pathlib import Path
from app.utils.exceptions import TopicAlreadyExistException


class Topics:
    def __init__(self):
        self.file_path: Path = Path(__file__).resolve().parents[2] / "data" / "topic_keywords.json"

    def add_topic(self, topic_name: str, topic_description: str):
        data: dict[str, dict[str, str]] = {}

        if self.file_path.exists():
            with open(self.file_path, mode="r", encoding="utf-8") as file:
                content = file.read().strip()
                if content:
                    data = json.loads(content)

        if topic_name in data:
            raise TopicAlreadyExistException(topic_name)

        data[topic_name] = {"description": topic_description}

        with open(self.file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)


class Emails:
    def __init__(self):
        self.file_path: Path = Path(__file__).resolve().parents[2] / "data" / "emails.json"

    def add_email(self, subject: str, body: str, topic: str | None = None) -> str:
        data: list[dict[str, str | None]] = []

        if self.file_path.exists():
            with open(self.file_path, mode="r", encoding="utf-8") as file:
                content = file.read().strip()
                if content:
                    data = json.loads(content)

        email_id = str(uuid.uuid4())
        email_payload: dict[str, str | None] = {
            "id": email_id,
            "subject": subject,
            "body": body,
            "topic": topic,
        }
        data.append(email_payload)

        with open(self.file_path, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

        return email_id

    def get_emails(self) -> list[dict[str, str | None]]:
        if not self.file_path.exists():
            return []

        with open(self.file_path, mode="r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []

        loaded = json.loads(content)
        if not isinstance(loaded, list):
            return []

        return loaded

    def get_labeled_emails(self) -> list[dict[str, str]]:
        labeled: list[dict[str, str]] = []
        for item in self.get_emails():
            subject = item.get("subject")
            body = item.get("body")
            topic = item.get("topic")
            if isinstance(subject, str) and isinstance(body, str) and isinstance(topic, str) and topic.strip():
                labeled.append({"subject": subject, "body": body, "topic": topic})

        return labeled

