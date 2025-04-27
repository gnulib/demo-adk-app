from google.adk.agents import Agent
import os
import sys

# Allow running from backend/ or project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import deckofcards_client

def _load_instructions():
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r", encoding="utf-8") as f:
        return f.read()

root_agent = Agent(
    name="simple_agent",
    model="gemini-2.0-flash",
    description=(
        "You are a helpful agent who can help users draw a deck of cards for a game."
    ),
    instruction=_load_instructions(),
    tools=[
        deckofcards_client.shuffle_new_deck,
        deckofcards_client.draw_cards,
        deckofcards_client.reshuffle_deck,
        deckofcards_client.new_unshuffled_deck,
        deckofcards_client.add_to_pile,
        deckofcards_client.list_pile,
        deckofcards_client.draw_from_pile,
        deckofcards_client.return_cards,
        deckofcards_client.return_cards_to_pile,
    ],
)
