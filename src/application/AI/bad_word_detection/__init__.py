from pydantic import BaseModel, Field
from typing import Literal

class BadWordDetection(BaseModel):
    """Bad Word Detection Result Model"""
    is_bad_word: Literal["no", "yes"] = Field(description="Indicates if bad words were detected.")

