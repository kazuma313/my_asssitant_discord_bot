from langgraph.graph import StateGraph, START, END
from langchain.messages import HumanMessage, SystemMessage
import logging
from .search_web import many_search_formatted
from .....domain.entities.agents.research.research import SectionState, SectionOutputState, Queries
from .....domain.templates.prompt.research.research_prompt_templates import (
    REPORT_SECTION_QUERY_GENERATOR_PROMPT,  
    SECTION_WRITER_PROMPT
    )


from infrastructure.AI.models.llm import get_llm_model
llm = get_llm_model(temperature=0.1)

def generate_queries(state: SectionState):
    """ Generate search queries for a specific report section """
    section = state["section"]
    logging.info('--- Generating Search Queries for Section: '+ section.name +' ---')
    number_of_queries = 5

    structured_llm = llm.with_structured_output(Queries)

    system_instructions = REPORT_SECTION_QUERY_GENERATOR_PROMPT.format(section_topic=section.description,
                                                                       number_of_queries=number_of_queries)

    user_instruction = "Generate search queries on the provided topic."
    search_queries = structured_llm.invoke([SystemMessage(content=system_instructions),
                                     HumanMessage(content=user_instruction)])
    logging.info('--- Generating Search Queries for Section: '+ section.name +' Completed ---')
    return {"search_queries": search_queries.queries} # type: ignore


async def search_web(state: SectionState):
    """ Search the web for each query, then return a list of raw sources and a formatted string of sources."""

    search_queries = state["search_queries"]
    logging.info('--- Searching Web for Queries ---')

    query_list = [query.search_query for query in search_queries]
    search_context = many_search_formatted(
                    query_list,
                    include_raw_content= True,
                    max_search_results = 5,
                    max_tokens= 4000,
                    search_depth = "advanced",
                    topic= "general",
                    model_name = "gpt-4"
                    )
    logging.info('--- Searching Web for Queries Completed ---')
    return {"source_str": search_context}


def write_section(state: SectionState):
    """ Write a section of the report """
    section = state["section"]
    source_str = state["source_str"]

    logging.info('--- Writing Section : '+ section.name +' ---')
    system_instructions = SECTION_WRITER_PROMPT.format(section_title=section.name,
                                                       section_topic=section.description,
                                                       context=source_str)

    user_instruction = "Generate a report section based on the provided sources."
    section_content = llm.invoke([SystemMessage(content=system_instructions),
                                  HumanMessage(content=user_instruction)])
    section.content = section_content.content # type: ignore
    logging.info('--- Writing Section : '+ section.name +' Completed ---')
    return {"completed_sections": [section]}


section_builder = StateGraph(SectionState, output=SectionOutputState) # type: ignore
section_builder.add_node("generate_queries", generate_queries)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)

section_builder.add_edge(START, "generate_queries")
section_builder.add_edge("generate_queries", "search_web")
section_builder.add_edge("search_web", "write_section")
section_builder.add_edge("write_section", END)
section_builder_subagent = section_builder.compile()