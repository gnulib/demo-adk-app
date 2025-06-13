from google.adk.tools import ToolContext
from .models import GameRoom
from demo_adk_app.utils.constants import StateVariables

def create_game(max_num_players: int, tool_context: ToolContext):
    """
    create a new game on behalf of the user
    Args:
        max_num_players: maximum number of players to allow joining the game
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
    # check if user is already enrolled in a game
    game_room_id = state.get(f"app:{user_id}_{StateVariables.CURRENT_GAME}", None)
    if game_room_id:
        return {
            "status" : "error",
            "message" : f"user id already enrolled with game room: {game_room_id}"
        }
    # create a new game room
    game_room_id = "1234" # todo: change with actual new id generation later
    game_room = GameRoom(
        game_room_id=game_room_id,
        host_user_id=user_id,
        players= [user_id],
        max_number_players=max_num_players,
        game_status="pre-game",
        current_turn_player_id = user_id # we start with host player
    )
    # set this game as the current game for user (app scope)
    state[f"app:{user_id}_{StateVariables.CURRENT_GAME}"] = game_room.game_room_id
    # also set the game as current game in session scope
    state[StateVariables.GAME_ROOM_ID] = game_room.game_room_id
    # mark user as host for current game (session scope)
    state[StateVariables.USER_ROLE] = "host"
    # add game details to application scope
    state[f"app:{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()
    # also add to current session state (session scope) to use with prompts
    state[StateVariables.GAME_DETAILS] = game_room.model_dump()
    return {
        "status" : "success",
        "message": f"created new game room: {game_room}"
    }

def join_game(game_room_id: str, tool_context: ToolContext):
    """
    join a new game as a player
    Args:
        game_room_id: a game room id to be provided by the user to join as a player
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
    # check if user is already enrolled in a game
    if state.get(f"app:{user_id}_{StateVariables.CURRENT_GAME}", None):
        game_room_id = state.get(f"app:{user_id}_{StateVariables.CURRENT_GAME}")
        return {
            "status" : "error",
            "message" : f"user id already enrolled with game room: {game_room_id}"
        }

    # check if game room exists (app scope)
    game_room_dict = state.get(f"app:{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }

    # convert to pydantic model
    game_room = GameRoom.model_validate(game_room_dict)

    # check if game has room for new player to join
    if game_room.max_num_players >= len(game_room.players):
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} has already reached max players"

        }
    # set this game as the current game for user (app scope)
    state[f"app:{user_id}_{StateVariables.CURRENT_GAME}"] = game_room.game_room_id
    # set the game room for current session
    state[StateVariables.GAME_ROOM_ID] = game_room.game_room_id
    # make the user as player of the game
    state[StateVariables.USER_ROLE] = "player"
    # add user to player list of the game room (application scope, to share with all users)
    game_room.players.append(user_id)
    # save the game room state
    state[f"app:{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()
    # also add to current session state (session scope) to use with prompts
    state[StateVariables.GAME_DETAILS] = game_room.model_dump()
    return {
        "status" : "success",
        "message" : f"added user as player for game room: {game_room}"
    }

def start_game(tool_context: ToolContext):
    """
    handle start game request by host of the game
    Args:
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    state = tool_context.state

def get_game_details(game_room_id: str, tool_context: ToolContext):
    """
    get details of the current game
    Args:
        tool_context: The ADK tool context.
    Returns:
        A status message from getting game details
    """
    state = tool_context.state
    # make sure that user id is available in session state
    # user_id = state.get(StateVariables.USER_ID, None)
    # if not user_id:
    #     return {
    #         "status" : "error",
    #         "message" : "user id is not known"
    #     }
    # check if game room exists (app scope)
    game_room_dict = state.get(f"app:{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }
    # return dtails of the game
    return {
        "status" : "success",
        "message" : game_room_dict
    }
