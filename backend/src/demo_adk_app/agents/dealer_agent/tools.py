
from google.adk.tools import ToolContext
from google.adk.sessions import State
from ..game_room_agent.models import GameRoom
from demo_adk_app.utils.constants import StateVariables
from demo_adk_app.utils import deckofcards_client

def start_game(game_room_id: str, tool_context: ToolContext):
    """
    handle start game request by host of the game
    Args:
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    state = tool_context.state
    # make sure that user id is available in session state
    user_id = state.get(StateVariables.USER_ID, None)
    if not user_id:
        return {
            "status" : "error",
            "message" : "user id is not known"
        }

    # check if game room exists (app scope)
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }

    # convert to pydantic model
    game_room = GameRoom.model_validate(game_room_dict)

    # check if game is in session (managed by game room agent)
    if game_room.game_status != "in-game":
        return {
            "status" : "error",
            "message" : "game is not yet started by the game room agent"
        }
    # initialize game score for each player and dealer
    game_room.player_scores={}
    for player in game_room.players:
        game_room.player_scores[player] = 0
    game_room.dealer_score = 0    

    # initialize player bets to zero
    game_room.bets={}

    # initialize a new full deck of card
    game_room.deck = deckofcards_client.shuffle_new_deck(deck_count=1, jokers_enabled=False)

    # set game status to "dealing"
    game_room.game_status = "dealing"

    # agent prompt will guide agent on how to handle dealing state
    # also will need to add new function / tool to handel player's bet
    # todo

    # save the game room state
    state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()
    # also add to current session state (session scope) to use with prompts
    state[StateVariables.GAME_DETAILS] = game_room.model_dump()
    # return nothing from function call so that
    # agent continue sprocessing request now that game is in session
    return None
