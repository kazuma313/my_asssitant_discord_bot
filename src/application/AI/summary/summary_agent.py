from langgraph.graph import StateGraph
from .nodes.summary import (
    generate_summary,
    collect_summaries,
    collapse_summaries,
    generate_final_summary,
    should_collapse,
)
from src.domain.entities.agents.summary_entities import OverallState
from .nodes.paralel_execution import map_summaries
from langgraph.graph import START, END


# Nodes:
graph = StateGraph(OverallState)
graph.add_node("generate_summary", generate_summary)  # same as before
graph.add_node("collect_summaries", collect_summaries)
graph.add_node("collapse_summaries", collapse_summaries)
graph.add_node("generate_final_summary", generate_final_summary)

# Edges:
graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
graph.add_edge("generate_summary", "collect_summaries")
graph.add_conditional_edges("collect_summaries", should_collapse)
graph.add_conditional_edges("collapse_summaries", should_collapse)
graph.add_edge("generate_final_summary", END)

summary_agent = graph.compile()
