from google.adk.agents import Agent
import os

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="concierge_agent",
    model="gemini-2.5-flash",
    description=(
        "Provides user assistance, answers FAQs, and helps with onboarding for the Blackjack application."
    ),
    instruction=_load_instructions(),
    tools=[],
)
