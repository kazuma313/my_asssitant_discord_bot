from langgraph.types import Send
from src.domain.entities.agents.research.research import ReportState

def parallelize_section_writing(state: ReportState):
    """ This is the "map" step when we kick off web research for some sections of the report in parallel and then write the section"""
    return [
        Send("section_builder_with_web_search", 
             {"section": s})
            for s in state["sections"]
              if s.research
    ]
    
def parallelize_final_section_writing(state: ReportState):
    """ Write any final sections using the Send API to parallelize the process """
    return [
        Send("write_final_sections",
             {"section": s, "report_sections_from_research": state["report_sections_from_research"]})
                 for s in state["sections"]
                    if not s.research
    ]
