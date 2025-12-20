from langchain_classic.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from src.domain.templates.prompt.summary_prompt_templates import map_prompt
from src.domain.entities.agents.summary import SummaryState, OverallState
from src.infrastructure.AI.models.llm import get_llm_model
from .utils import length_function, token_max, _reduce
from langchain_core.documents import Document
from typing import Literal
import logging

llm = get_llm_model(temperature=0.1)


async def generate_summary(state: SummaryState):
    logging.info("=== GENERATE SUMMARY ===")
    prompt = map_prompt.invoke(state["content"])  # type: ignore
    response = await llm.ainvoke(prompt)
    return {"summaries": [response.content]}


async def collapse_summaries(state: OverallState):
    logging.info("=== COLLAPSING SUMMARIES ===")
    doc_lists = split_list_of_docs(
        state["collapsed_summaries"], length_function, token_max
    )
    results = []
    for doc_list in doc_lists:
        results.append(await acollapse_docs(doc_list, _reduce))  # type: ignore
    return {"collapsed_summaries": results}


def collect_summaries(state: OverallState):
    logging.info("=== COLLECTED SUMMARIES ===")
    return {
        "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
    }


async def generate_final_summary(state: OverallState):
    logging.info("=== GENERATE FINAL SUMMARY ===")
    response = await _reduce(state["collapsed_summaries"])  # type: ignore
    return {"final_summary": response}


def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = length_function(state["collapsed_summaries"])
    if num_tokens > token_max:
        return "collapse_summaries"
    else:
        return "generate_final_summary"
