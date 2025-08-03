from pydantic import BaseModel, HttpUrl
from typing import List

class HackRxRequest(BaseModel):
    documents: HttpUrl  # Pydantic will validate that this is a valid URL
    questions: List[str]

class HackRxResponse(BaseModel):
    answers: List[str]
