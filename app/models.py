from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import secrets

class ToxicityRequest(BaseModel):
    texts: List[str] = Field(
        ..., 
        max_items=1000,
        description="List of texts to analyze"
    )
    batch_size: Optional[int] = Field(
        default=32,
        ge=1,
        le=128,
        description="Batch size for processing"
    )

class ToxicityResult(BaseModel):
    toxicity: float = Field(..., ge=0.0, le=1.0)
    severe_toxicity: float = Field(..., ge=0.0, le=1.0)
    obscene: float = Field(..., ge=0.0, le=1.0)
    threat: float = Field(..., ge=0.0, le=1.0)
    insult: float = Field(..., ge=0.0, le=1.0)
    identity_attack: float = Field(..., ge=0.0, le=1.0)

class ToxicityResponse(BaseModel):
    results: List[ToxicityResult]
    processing_time: float
    request_id: str = Field(default_factory=lambda: secrets.token_urlsafe(8))
    timestamp: datetime = Field(default_factory=datetime.utcnow)