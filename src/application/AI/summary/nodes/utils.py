from src.domain.templates.prompt.summary_prompt_templates import reduce_prompt
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from typing import List

token_max = 5000
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def length_function(documents: List[Document]) -> int:
    """Get number of tokens for input contents."""
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)


async def _reduce(input: dict) -> str:
    prompt = reduce_prompt.invoke(input)
    response = await llm.ainvoke(prompt)
    return response.content  # type: ignore
