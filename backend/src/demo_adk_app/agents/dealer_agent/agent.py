from google.adk.agents import Agent
import os

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="dealer_agent",
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "Executes Blackjack gameplay: manages deck, deals cards, processes player actions, determines outcomes."
    ),
    instruction=_load_instructions(),
    tools=[],
)
