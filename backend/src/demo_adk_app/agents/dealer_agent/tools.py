
from google.adk.tools import ToolContext
from google.adk.sessions import State
from ...utils.models import GameRoom
from ...utils.tools import _load_game_room, _save_game_room
from demo_adk_app.utils.constants import StateVariables
from demo_adk_app.utils import deckofcards_client

def initialize_game_room(game_room_id: str, tool_context: ToolContext):
    """
    initialize game room at the start of the game
    Args:
        game_room_id: a game room id to start the game
        tool_context: The ADK tool context.
    Returns:
        A status message from handling initialization request
    """

    # load game room object
    game_room, error = _load_game_room(game_room_id, tool_context)
    if error:
        return error

    # check if game is still in pre-game session (managed by game room agent)
    if game_room.game_status == "pre-game":
        return {
            "status" : "error",
            "message" : "game is not yet started by the game room agent"
        }

    # initialize game for each player
    game_room.player_scores={}
    for player in game_room.players:
        game_room.player_scores[player] = 0
        game_room.player_cards[player] = []

    # set game status to "dealing"
    game_room.game_status = "dealing"

    # agent prompt will guide agent on how to handle dealing state
    # also will need to add new function / tool to handel player's bet
    # todo

    # save the game room state
    _save_game_room(game_room, tool_context)
 
    # following memory updates should be take care by the agent itself as needed
    # # also add to current session state (session scope) to use with prompts
    # state[StateVariables.GAME_DETAILS] = game_room.model_dump()
 
    # return the game room details, agent will memorize as needed
    return {
        "status" : "success",
        "game_room": game_room
    }

def create_deck_tool(game_room_id: str, tool_context: ToolContext):
    """
    creat a new shuffled deck of card for the game
    Args:
        game_room_id: a game room id to for this deck of card
        tool_context: The ADK tool context.
    Returns:
        A list of cards in the deck
    """
    # load game room object
    game_room: GameRoom = None
    error: dict = None
    game_room, error = _load_game_room(game_room_id, tool_context)
    if error:
        return error

    # create a new deck of cards for this game room
    deck = deckofcards_client.shuffle_new_deck(deck_count=1, jokers_enabled=False, cards=None)
    if not "success" in deck or not deck["success"]:
        return {
            "status" : "error",
            "mesage" : f"failed to create new deck: {deck}"
        }    
    else:
        game_room.deck = deck

    # save game room object
    _save_game_room(game_room, tool_context)

    return {
        "status" : "success",
        "message" : "new deck of cards created"
    }

def shuffle_deck_tool(game_room_id: str, tool_context):
    """
    shuffles deck of card for the game
    Args:
        game_room_id: a game room id to for this deck of card
        tool_context: The ADK tool context.
    Returns:
        A shuffled deck of cards
    """
    # NO OP, deck sould already be shuffled, will just return None
    return {
        "status" : "success",
        "message" : "deck is shuffled"
    }

def draw_card_tool(game_room_id: str, tool_context):
    """
    draw 1 card from the deck of cards
    Args:
        game_room_id: a game room id to for this deck of card
        tool_context: The ADK tool context.
    Returns:
        Top card from the deck
    """
    # load game room object
    game_room: GameRoom = None
    error: dict = None
    game_room, error = _load_game_room(game_room_id, tool_context)
    if error:
        return error

    # draw 1 card from the deck
    cards = deckofcards_client.draw_cards(game_room.deck["deck_id"], 1)
    if not "success" in cards or not cards["success"]:
        return {
            "status" : "error",
            "mesage" : f"failed to draw cards from deck: {cards}"
        }
    else:
        # return the card
        card = cards["cards"][0]
        return {"value" : card["value"], "code" : card["code"], "suit" : card["suit"]}

def calculate_card_value(card: dict):
    """
    calculate value of a standlone card
    Args:
        card: card object to evaluate
    Returns:
        value of the card
    """
    value_str = card['value']
    if value_str in ['JACK', 'QUEEN', 'KING']:
        return 10
    elif value_str == 'ACE':
        return 11
    else:
        return int(value_str)


def calculate_hand_score(player_hand: list[dict]):
    """
    calculate value of a card, based on player's hand
    Args:
        player_hand: list of card objects in a player's hand
    Returns:
        score of player's hand based on all cards
    """
    score = 0
    num_aces = 0
    # first calculate score based on each card's standalone value
    for card in player_hand:
        card_value = calculate_card_value(card)
        # also keep track of number of aces
        if card_value == 11:
            num_aces += 1
        score += card_value

    # now adjust score based on ACEs to optimum value
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1

    return score