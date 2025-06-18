from google.adk.agents import Agent
from .prompt import PROMPT
from demo_adk_app.utils.tools import memorize
from demo_adk_app.utils.constants import Models

root_agent = Agent(
    name="user_profile_agent",
    model=Models.ECO_MODEL,
    description=(
        "Manages user identity, authentication, and persistent profile data in Firebase."
    ),
    instruction=PROMPT,
    tools=[memorize],
)
