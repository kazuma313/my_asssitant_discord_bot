builder = StateGraph(ReportState, input=ReportStateInput, output=ReportStateOutput)

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


if __name__ == "__main__":
    from IPython.display import display
    from rich.console import Console
    from rich.markdown import Markdown as RichMarkdown

    async def call_planner_agent(agent, prompt, config={"recursion_limit": 50}, verbose=False):
        events = agent.astream(
            {'topic' : prompt},
            config,
            stream_mode="values",
        )

        async for event in events:
            for k, v in event.items():
                if verbose:
                    if k != "__end__":
                        display(RichMarkdown(repr(k) + ' -> ' + repr(v)))
                if k == 'final_report':
                    print('='*50)
                    print('Final Report:')
                    md = RichMarkdown(v)
                    display(md)
                    
    topic = "Detailed report on how to build Agentic AI systems, design patterns and current frameworks"
    await call_planner_agent(agent=reporter_agent,
                            prompt=topic)