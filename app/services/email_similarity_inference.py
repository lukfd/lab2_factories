from typing import Dict, Any

from app.dataclasses import Email
from app.features.factory import FeatureGeneratorFactory
from app.models.similarity_model import EmailClassifierModel
from app.utils.files import Emails


class EmailSimilarityInferenceService:
    """Service that classifies emails using nearest labeled stored email similarity."""

    def __init__(self):
        self.model = EmailClassifierModel()
        self.feature_factory = FeatureGeneratorFactory()
        self.email_store = Emails()

    def classify_email(self, email: Email) -> Dict[str, Any]:
        features = self.feature_factory.generate_all_features(email)
        labeled_emails = self.email_store.get_labeled_emails()

        if not labeled_emails:
            raise ValueError("No labeled emails found. Store emails with a topic before using nearest strategy.")

        predicted_topic, similarity = self.model.predict_from_nearest_email(features, labeled_emails)
        if predicted_topic is None:
            raise ValueError("Could not classify using nearest strategy.")

        return {
            "predicted_topic": predicted_topic,
            "topic_scores": {predicted_topic: float(similarity)},
            "features": features,
            "available_topics": self.model.topics,
            "email": email,
        }
