from src.application.usecases.calling_agent import call_agent
from src.application.AI.research.research_agent import reporter_agent


async def research_topic(topic: str):
    param = {"topic": topic}
    result = await call_agent(agent=reporter_agent, param=param)
    return result
