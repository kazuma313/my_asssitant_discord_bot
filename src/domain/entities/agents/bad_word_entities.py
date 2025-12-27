from pydantic import BaseModel, Field
from typing import Literal

class BadWordDetection(BaseModel):
    """Bad Word Detection Result Model"""
    is_bad_word: Literal["yes", "no"] = Field(description="'yes' jika kata kasar atau sarkas, dan 'no' jika kata tidak kasar atau sarkas")

