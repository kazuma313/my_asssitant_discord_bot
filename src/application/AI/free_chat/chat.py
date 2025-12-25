from langchain.messages import HumanMessage, SystemMessage
from src.infrastructure.AI.models.llm import get_llm_model
from src.domain.templates.prompt.free_chat_prompt_template import systems_chat_prompt

llm = get_llm_model(temperature=0.1)


def free_chat_prompt_to_messages(prompt_usr: str, name: str = "", id: str = ""):
    """Convert free chat prompt to list of HumanMessage"""
    system_prompt = SystemMessage(content=systems_chat_prompt)
    user_prompt = HumanMessage(content=prompt_usr, name=name, id=id)
    messages = [system_prompt, user_prompt]
    return llm.invoke(messages)
