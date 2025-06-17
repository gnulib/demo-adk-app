from google.adk.agents import Agent
from .prompt import PROMPT
from demo_adk_app.utils.tools import memorize

root_agent = Agent(
    name="user_profile_agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Manages user identity, authentication, and persistent profile data in Firebase."
    ),
    instruction=PROMPT,
    tools=[memorize],
)
