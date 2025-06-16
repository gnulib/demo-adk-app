
from google.adk.tools import ToolContext
from google.adk.sessions import State
from ..game_room_agent.models import GameRoom
from demo_adk_app.utils.constants import StateVariables
from demo_adk_app.utils import deckofcards_client

def _load_game_room(game_room_id: str, tool_context: ToolContext):
    """
    utility method to load game room object
    Args:
        game_room_id: a game room id to load the game
        tool_context: The ADK tool context.
    Returns:
        game_room: if successfule
        error: if failure
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return None, {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }

    # convert to pydantic model
    game_room = GameRoom.model_validate(game_room_dict)
    return game_room, None

def _save_game_room(game_room: GameRoom, tool_context: ToolContext):
    """
    utility method to save game room object
    Args:
        game_room: a game room object to save
        tool_context: The ADK tool context.
    Returns:
        None
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()


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

    # initialize a new full deck of card
    game_room.deck = deckofcards_client.shuffle_new_deck(deck_count=1, jokers_enabled=False, cards=None)

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

def deal_card(game_room_id: str, deck_id: str, player_id: str, tool_context: ToolContext):
    """
    deal 1 card to a player in a game
    Args:
        game_room_id: a game room id for the game
        deck_id: deck id from the deck in game room
        player_id: a user id of the player to deal the card
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """

    # load game room object
    game_room, error = _load_game_room(game_room_id, tool_context)
    if error:
        return error

    # make sure player is in the game
    if player_id not in game_room.players:
        return {
            "status" : "error",
            "message" : "player is not part of the game's players list"
        }

    # deal a card to the player
    game_room.player_cards[player_id].append(deckofcards_client.draw_cards(deck_id, 1))

    # save game room
    _save_game_room(game_room, tool_context)

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

    # draw all 52 cards and return back the cards
    cards = deckofcards_client.draw_cards(game_room.deck["deck_id"], 52)
    if not "success" in cards or not cards["success"]:
        return {
            "status" : "error",
            "mesage" : f"failed to draw cards from deck: {cards}"
        }
    else:
        game_room.cards = cards["cards"]

    # save game room object
    _save_game_room(game_room, tool_context)

    # return the list of cards
    return game_room.cards


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
    return None

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

    # pop the top card from deck
    card = game_room.cards.pop()

    # save game room object
    _save_game_room(game_room, tool_context)

    # return the card
    return card
