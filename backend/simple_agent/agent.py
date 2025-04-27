from google.adk.agents import Agent
import os

from backend.utils.deckofcards_client import (
    shuffle_new_deck,
    draw_cards,
    reshuffle_deck,
    new_unshuffled_deck,
    add_to_pile,
    list_pile,
    draw_from_pile,
    return_cards,
    return_cards_to_pile,
)

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="simple-agent",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful agent who can help users draw a deck of cards for a game."
    ),
    instruction=_load_instructions(),
    tools=[
        shuffle_new_deck,
        draw_cards,
        reshuffle_deck,
        new_unshuffled_deck,
        add_to_pile,
        list_pile,
        draw_from_pile,
        return_cards,
        return_cards_to_pile,
    ],
)
