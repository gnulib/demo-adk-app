from google.adk.agents import Agent
from .prompt import PROMPT
from demo_adk_app.utils.tools import memorize
from .tools import (
    create_game,
    join_game,
    start_game,
    get_game_details

)

root_agent = Agent(
    name="game_room_agent",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Manages Blackjack game room lifecycle: creation, player joining/leaving, status tracking via Firebase."
    ),
    instruction=PROMPT,
    tools=[memorize, create_game, join_game, start_game, get_game_details],
)
