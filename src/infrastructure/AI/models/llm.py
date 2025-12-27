from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4o-mini")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY not found! "
        "Please set it in .env file or environment variables"
    )


def get_llm_model(temperature, model_name: str = "gpt-4o-mini-2024-07-18"):
    return ChatOpenAI(model=model_name, 
                      temperature=temperature,
                      max_tokens=1500)
