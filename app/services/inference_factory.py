from app.services.email_similarity_inference import EmailSimilarityInferenceService
from app.services.email_topic_inference import EmailTopicInferenceService


class InferenceServiceFactory:
    """Factory to create an inference service based on strategy."""

    @staticmethod
    def create(strategy: str):
        if strategy == "nearest":
            return EmailSimilarityInferenceService()
        return EmailTopicInferenceService()
