from google.adk.agents import Agent
from .prompt import PROMPT
from demo_adk_app.utils.constants import Models

root_agent = Agent(
    name="concierge_agent",
    model=Models.ECO_MODEL,
    description=(
        "Provides user assistance, answers FAQs, and helps with onboarding for the Blackjack application."
    ),
    instruction=PROMPT,
    tools=[],
)
