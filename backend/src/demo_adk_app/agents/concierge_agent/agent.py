from google.adk.agents import Agent
from .prompt import PROMPT

root_agent = Agent(
    name="concierge_agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Provides user assistance, answers FAQs, and helps with onboarding for the Blackjack application."
    ),
    instruction=PROMPT,
    tools=[],
)
