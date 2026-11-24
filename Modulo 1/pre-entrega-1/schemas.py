from typing import Literal
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal['system', 'user', 'assistant']
    content: str = Field(min_length=1)


class ModelConfig(BaseModel):
    provider: Literal['openai', 'anthropic']
    model: str = Field(min_length=1)
    temperature: float = Field(default=0.5, ge=0, le=2)
    max_tokens: int = Field(default=256, gt=0)
    timeout: float = Field(default=30, gt=0)


class ModelResponse(BaseModel):
    provider: str
    model: str
    content: str = ''
    error: str | None = None
