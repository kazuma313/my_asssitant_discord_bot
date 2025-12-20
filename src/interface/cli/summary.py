from src.application.usecases.calling_agent import call_agent
from src.application.AI.summary.summary_agent import summary_agent

topic = "Detailed report on how to build Agentic AI systems, design patterns and current frameworks"
params = {"contents": [""]}
result = await call_agent(agent=summary_agent, param=params)
