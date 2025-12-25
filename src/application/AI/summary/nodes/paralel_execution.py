from src.domain.entities.agents.summary_entities import OverallState
from langgraph.types import Send


def map_summaries(state: OverallState):
    return [
        Send("generate_summary", {"content": content}) for content in state["contents"]
    ]
