from google.adk.agents import Agent
import os
from demo_adk_app.agents.game_room_agent.agent import root_agent as game_room_agent
from demo_adk_app.agents.dealer_agent.agent import root_agent as dealer_agent
from demo_adk_app.agents.user_profile_agent.agent import root_agent as user_profile_agent
from demo_adk_app.agents.concierge_agent.agent import root_agent as concierge_agent

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="game_master_agent",
    model="gemini-2.5-pro",
    description=(
        "The central orchestrator for the Blackjack application, managing game flow and coordinating sub-agents."
    ),
    instruction=_load_instructions(),
    tools=[],
    sub_agents=[
        game_room_agent,
        dealer_agent,
        user_profile_agent,
        concierge_agent,
    ],
)
