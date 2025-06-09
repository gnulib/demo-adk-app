from google.adk.agents import Agent
import os

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="game_room_agent",
    model="gemini-2.5-flash",
    description=(
        "Manages Blackjack game room lifecycle: creation, player joining/leaving, status tracking via Firebase."
    ),
    instruction=_load_instructions(),
    tools=[],
)
