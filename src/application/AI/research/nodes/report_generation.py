from langchain.messages import HumanMessage, SystemMessage
import logging
from .search_web import many_search_formatted
from src.domain.entities.agents.research_entites import (
    Section,
    SearchQuery,
    Sections,
    Queries,
    ReportState,
    SectionState,
)

from src.domain.templates.prompt.research_prompt_templates import (
    DEFAULT_REPORT_STRUCTURE,
    REPORT_PLAN_QUERY_GENERATOR_PROMPT,
    REPORT_PLAN_SECTION_GENERATOR_PROMPT,
    FINAL_SECTION_WRITER_PROMPT,
)

from src.infrastructure.AI.models.llm import get_llm_model

llm = get_llm_model(temperature=0.1)


async def generate_report_plan(state: ReportState):
    """Generate the overall plan for building the report"""
    topic = state["topic"]

    report_structure = DEFAULT_REPORT_STRUCTURE
    number_of_queries = 8

    structured_llm = llm.with_structured_output(Queries)

    system_instructions_query = REPORT_PLAN_QUERY_GENERATOR_PROMPT.format(
        topic=topic,
        report_organization=report_structure,
        number_of_queries=number_of_queries,
    )

    try:
        results = structured_llm.invoke(
            [
                SystemMessage(content=system_instructions_query),
                HumanMessage(
                    content="Generate search queries that will help with planning the sections of the report."
                ),
            ]
        )
        query_list = [
            query.search_query if isinstance(query, SearchQuery) else str(query)
            for query in results.queries  # type: ignore
        ]

        search_context = many_search_formatted(
            query_list,
            include_raw_content=True,
            max_search_results=5,
            max_tokens=1000,
            search_depth="advanced",
            topic="general",
            model_name="gpt-4",
        )

        structured_llm = llm.with_structured_output(Sections)
        system_instructions_sections = REPORT_PLAN_SECTION_GENERATOR_PROMPT.format(
            topic=topic,
            report_organization=report_structure,
            search_context=search_context,
        )
        report_sections = structured_llm.invoke(
            [
                SystemMessage(content=system_instructions_sections),
                HumanMessage(
                    content="Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. Each section must have: name, description, plan, research, and content fields."
                ),
            ]
        )

        logging.info("--- Generating Report Plan Completed ---")
        return {"sections": report_sections.sections}  # type: ignore

    except Exception as e:
        logging.error(f"Error in generate_report_plan: {e}")
        return {"sections": []}


def format_completed_sections(state: ReportState):
    """Gather completed sections from research and format them as context for writing the final sections"""

    def format_sections(sections: list[Section]) -> str:
        """Format a list of report sections into a single text string"""
        formatted_str = ""
        for idx, section in enumerate(sections, 1):
            formatted_str += f"""
            {'='*60}
            Section {idx}: {section.name}
            {'='*60}
            Description:
            {section.description}
            Requires Research:
            {section.research}

            Content:
            {section.content if section.content else '[Not yet written]'}
            """
        return formatted_str

    logging.info("--- Formatting Completed Sections ---")
    completed_sections = state["completed_sections"]
    completed_report_sections = format_sections(completed_sections)
    logging.info("--- Formatting Completed Sections is Done ---")

    return {"report_sections_from_research": completed_report_sections}


def write_final_sections(state: SectionState):
    """Write the final sections of the report, which do not require web search and use the completed sections as context"""

    section = state["section"]
    completed_report_sections = state["report_sections_from_research"]
    logging.info("--- Writing Final Section: " + section.name + " ---")
    system_instructions = FINAL_SECTION_WRITER_PROMPT.format(
        section_title=section.name,
        section_topic=section.description,
        context=completed_report_sections,
    )

    user_instruction = "Craft a report section based on the provided sources."
    section_content = llm.invoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(content=user_instruction),
        ]
    )

    section.content = section_content.content  # type: ignore
    logging.info("--- Writing Final Section: " + section.name + " Completed ---")
    return {"completed_sections": [section]}


def compile_final_report(state: ReportState):
    """Compile the final report"""

    sections = state["sections"]
    completed_sections = {s.name: s.content for s in state["completed_sections"]}
    logging.info("--- Compiling Final Report ---")

    for section in sections:
        section.content = completed_sections[section.name]

    all_sections = "\n\n".join([s.content for s in sections])
    formatted_sections = all_sections.replace("\\$", "TEMP_PLACEHOLDER")
    formatted_sections = formatted_sections.replace("$", "\\$")
    formatted_sections = formatted_sections.replace("TEMP_PLACEHOLDER", "\\$")
    logging.info("--- Compiling Final Report Done ---")

    return {"final_report": formatted_sections}
