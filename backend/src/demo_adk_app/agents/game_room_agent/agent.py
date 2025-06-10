from google.adk.agents import Agent
from .prompt import PROMPT

root_agent = Agent(
    name="game_room_agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Manages Blackjack game room lifecycle: creation, player joining/leaving, status tracking via Firebase."
    ),
    instruction=PROMPT,
    tools=[],
)
