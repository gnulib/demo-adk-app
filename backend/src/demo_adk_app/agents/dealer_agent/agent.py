from google.adk.agents import Agent
from .prompt import PROMPT
from .tools import (
    initialize_game_room, create_deck_tool, shuffle_deck_tool, draw_card_tool,
    calculate_card_value, calculate_hand_score
)
from demo_adk_app.utils.tools import memorize
from demo_adk_app.utils.constants import Models

root_agent = Agent(
    name="dealer_agent",
    # model="gemini-2.5-pro-preview-05-06",
    model=Models.FLASH_MODEL,
    description=(
        "Executes Blackjack gameplay: manages deck, deals cards, processes player actions, determines outcomes."
    ),
    instruction=PROMPT,
    tools=[
        memorize,
        initialize_game_room,
        create_deck_tool,
        shuffle_deck_tool,
        draw_card_tool,
        calculate_card_value,
        calculate_hand_score,
    ],
)
