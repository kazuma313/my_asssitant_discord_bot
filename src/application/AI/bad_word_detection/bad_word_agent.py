from ...prompt.bad_word_prompte_template import BAD_WORD_PROMPT
from src.domain.entities.agents.bad_word_entities import BadWordDetection
from src.infrastructure.AI.models.llm import get_llm_model
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from typing import TypedDict
from langchain.agents.structured_output import ToolStrategy
# from langchain.agents.structured_output import ProviderStrategy

llm = get_llm_model(temperature=0.1, model_name="gpt-3.5-turbo-0125")

class Text2Classify(TypedDict):
    level: str
    
@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    level_of_check = request.runtime.context.get("level", "basic")
    base_prompt = BAD_WORD_PROMPT
    if level_of_check == "basic":
        return base_prompt
    return base_prompt


KLASIFIKASI_BAD_WORD = create_agent(
    model=llm,
    tools=[],
    middleware=[user_role_prompt], 
    context_schema=Text2Classify,
    response_format=ToolStrategy(schema=BadWordDetection,
                                 handle_errors=True)
)
