from google.adk.agents import Agent
from demo_adk_app.agents.game_room_agent.agent import root_agent as game_room_agent
from demo_adk_app.agents.dealer_agent.agent import root_agent as dealer_agent
from demo_adk_app.agents.user_profile_agent.agent import root_agent as user_profile_agent
from demo_adk_app.agents.concierge_agent.agent import root_agent as concierge_agent
from demo_adk_app.utils.tools import memorize

from .prompt import PROMPT, SYSTEM_PROMPT

root_agent = Agent(
    name="game_master_agent",
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "The central orchestrator for the Blackjack application, managing game flow and coordinating sub-agents."
    ),
    instruction=PROMPT,
    global_instruction=SYSTEM_PROMPT,
    tools=[memorize],
    sub_agents=[
        game_room_agent,
        dealer_agent,
        user_profile_agent,
        concierge_agent,
    ],
)
