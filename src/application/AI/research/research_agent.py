from .nodes.paralel_execution import parallelize_final_section_writing, parallelize_section_writing
from .nodes.report_generation import generate_report_plan
from .nodes.section_report import section_builder_subagent
from .nodes.report_generation import format_completed_sections, write_final_sections, compile_final_report
from langgraph.graph import StateGraph, START, END
from domain.entities.agents.research.research import ReportState, ReportStateInput, ReportStateOutput

builder = StateGraph(ReportState, input_schema=ReportStateInput, output_schema=ReportStateOutput)
builder.add_node("generate_report_plan", generate_report_plan)
builder.add_node("section_builder_with_web_search", section_builder_subagent)
builder.add_node("format_completed_sections", format_completed_sections)
builder.add_node("write_final_sections", write_final_sections)
builder.add_node("compile_final_report", compile_final_report)

builder.add_edge(START, "generate_report_plan")
builder.add_conditional_edges("generate_report_plan",
                              parallelize_section_writing,
                              ["section_builder_with_web_search"])
builder.add_edge("section_builder_with_web_search", "format_completed_sections")
builder.add_conditional_edges("format_completed_sections",
                              parallelize_final_section_writing,
                              ["write_final_sections"])
builder.add_edge("write_final_sections", "compile_final_report")
builder.add_edge("compile_final_report", END)

reporter_agent = builder.compile()