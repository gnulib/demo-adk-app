from google.adk.agents import Agent
from .prompt import PROMPT
from demo_adk_app.utils.tools import memorize
from .tools import (
    create_game,
    join_game,
    leave_game,
    start_game,
    get_game_details

)
from demo_adk_app.utils.constants import Models

root_agent = Agent(
    name="game_room_agent",
    model=Models.FLASH_MODEL,
    description=(
        "Manages Blackjack game room lifecycle: creation, player joining/leaving, status tracking via Firebase."
    ),
    instruction=PROMPT,
    tools=[memorize, create_game, join_game, leave_game, start_game, get_game_details],
)
