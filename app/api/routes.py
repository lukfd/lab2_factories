from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator, Field
from typing import Dict, Any, List, Optional
from app.services.email_topic_inference import EmailTopicInferenceService
from app.services.inference_factory import InferenceServiceFactory
from app.dataclasses import Email
from app.utils.files import Topics, Emails
from app.utils.exceptions import TopicAlreadyExistException

router = APIRouter()

class ClassificationStrategies(Enum):
    TOPIC = "topic"
    NEAREST = "nearest"

class EmailClassifyRequest(BaseModel):
    subject: str
    body: str
    strategy: ClassificationStrategies = Field(default=ClassificationStrategies.TOPIC)

class EmailWithTopicRequest(BaseModel):
    subject: str
    body: str
    topic: Optional[str] = None

    @field_validator("subject", "body")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field cannot be empty")
        return value

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("topic cannot be empty when provided")
        return value

class EmailClassificationResponse(BaseModel):
    predicted_topic: str
    topic_scores: Dict[str, float]
    features: Dict[str, Any]
    available_topics: List[str]

class EmailAddResponse(BaseModel):
    message: str
    email_id: str

@router.post("/emails", response_model=EmailAddResponse)
async def store_email(request: EmailWithTopicRequest):
    try:
        emails = Emails()
        email_id = emails.add_email(
            subject=request.subject,
            body=request.body,
            topic=request.topic,
        )
        return EmailAddResponse(message="Email stored successfully", email_id=email_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/emails/classify", response_model=EmailClassificationResponse)
async def classify_email(request: EmailClassifyRequest):
    try:
        inference_service = InferenceServiceFactory.create(request.strategy.value)
        email = Email(subject=request.subject, body=request.body)
        result = inference_service.classify_email(email)
        
        return EmailClassificationResponse(
            predicted_topic=result["predicted_topic"],
            topic_scores=result["topic_scores"],
            features=result["features"],
            available_topics=result["available_topics"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def topics():
    """Get available email topics"""
    inference_service = EmailTopicInferenceService()
    info = inference_service.get_pipeline_info()
    return {"topics": info["available_topics"]}


class Topic(BaseModel):
    name: str
    description: str

    @field_validator("name")
    @classmethod
    def validate_single_word_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name cannot be empty")
        if any(char.isspace() for char in value):
            raise ValueError("name must be a single word")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("description cannot be empty")
        return value


@router.post("/topic")
async def create_new_topic(
    topic: Topic
):
    """Add a new topic"""
    try:
        topics = Topics()
        topics.add_topic(topic.name, topic.description)
        return topic
    except TopicAlreadyExistException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/pipeline/info") 
async def pipeline_info():
    inference_service = EmailTopicInferenceService()
    return inference_service.get_pipeline_info()

# TODO: LAB ASSIGNMENT - Part 2 of 2  
# Create a GET endpoint at "/features" that returns information about all feature generators
# available in the system.
#
# Requirements:
# 1. Create a GET endpoint at "/features"
# 2. Import FeatureGeneratorFactory from app.features.factory
# 3. Use FeatureGeneratorFactory.get_available_generators() to get generator info
# 4. Return a JSON response with the available generators and their feature names
# 5. Handle any exceptions with appropriate HTTP error responses
#
# Expected response format:
# {
#   "available_generators": [
#     {
#       "name": "spam",
#       "features": ["has_spam_words"]
#     },
#     ...
#   ]
# }
#
# Hint: Look at the existing endpoints above for patterns on error handling
# Hint: You may need to instantiate generators to get their feature names

