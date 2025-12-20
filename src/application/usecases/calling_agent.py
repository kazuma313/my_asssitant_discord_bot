async def call_agent(agent, param, config={"recursion_limit": 50}):
    events = await agent.ainvoke(
        param,
        config,
    )
    return events