from google.adk.agents import Agent
from .prompt import PROMPT
from .tools import start_game

root_agent = Agent(
    name="dealer_agent",
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "Executes Blackjack gameplay: manages deck, deals cards, processes player actions, determines outcomes."
    ),
    instruction=PROMPT,
    tools=[
        start_game,
    ],
)
