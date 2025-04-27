from google.adk.agents import Agent

root_agent = Agent(
    name="simple-agent",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful agent who can help users draw a deck of cards for a game."
    ),
    instruction=(
        "You are a helpful agent who can help users draw a deck of cards for a game."
    ),
    tools=[],
)