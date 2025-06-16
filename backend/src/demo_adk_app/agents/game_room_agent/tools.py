from google.adk.tools import ToolContext
from google.adk.sessions import State
from .models import GameRoom
from demo_adk_app.utils.constants import StateVariables

def create_game(game_room_id: str, user_id: str, tool_context: ToolContext):
    """
    create a new game on behalf of the user
    Args:
        game_room_id: user provided id for game room
        user_id : user id of the player hosting the game
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    # hardcoding to 1 -- we'll only have single player mode for MVP
    max_num_players: int = 1

    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if user is already enrolled in a game
    # TODO: replace this from "app:" scope to DB store
    old_game_room_id = state.get(f"{State.APP_PREFIX}{user_id}_{StateVariables.CURRENT_GAME}", None)
    if old_game_room_id:
        return {
            "status" : "error",
            "message" : f"user id already enrolled with game room: {old_game_room_id}"
        }

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} already exists"
        }

    # create a new game room
    game_room = GameRoom(
        game_room_id=game_room_id,
        host_user_id=user_id,
        players= [user_id],
        max_number_players=max_num_players,
    )
    # set this game as the current game for user (app scope)
    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{user_id}_{StateVariables.CURRENT_GAME}"] = game_room.game_room_id

    # following memory updates should be take care by the agent itself as needed
    # # also set the game as current game in session scope
    # state[StateVariables.GAME_ROOM_ID] = game_room.game_room_id
    # # mark user as host for current game (session scope)
    # state[StateVariables.USER_ROLE] = "host"
    # # also add to current session state (session scope) to use with prompts
    # state[StateVariables.GAME_DETAILS] = game_room.model_dump()

    # add game details to application scope
    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()

    # return the game room details, agent will memorize as needed
    return {
        "status" : "success",
        "game_room": game_room
    }

def join_game(game_room_id: str, user_id: str, tool_context: ToolContext):
    """
    join a new game as a player
    Args:
        game_room_id: a game room id to be provided by the user to join as a player
        user_id : user id of the player requesting to join the game
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if user is already enrolled in a game
    # TODO: replace this from "app:" scope to DB store
    if state.get(f"{State.APP_PREFIX}{user_id}_{StateVariables.CURRENT_GAME}", None):
        game_room_id = state.get(f"{State.APP_PREFIX}{user_id}_{StateVariables.CURRENT_GAME}")
        return {
            "status" : "error",
            "message" : f"user id already enrolled with game room: {game_room_id}"
        }

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
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

    # check that game is still accepting players
    if game_room.game_status != "pre-game":
        return {
            "status" : "error",
            "message" : f"game is not accepting new players, status is {game_room.game_status}"
        }

    # set this game as the current game for user (app scope)
    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{user_id}_{StateVariables.CURRENT_GAME}"] = game_room.game_room_id

    # following memory updates should be take care by the agent itself as needed
    # # set the game room for current session
    # state[StateVariables.GAME_ROOM_ID] = game_room.game_room_id
    # # make the user as player of the game
    # state[StateVariables.USER_ROLE] = "player"
    # # also add to current session state (session scope) to use with prompts
    # state[StateVariables.GAME_DETAILS] = game_room.model_dump()

    # add user to player list of the game room (application scope, to share with all users)
    game_room.players.append(user_id)

    # save the game room state
    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()

    # return the game room details, agent will memorize as needed
    return {
        "status" : "success",
        "game_room": game_room
    }

def start_game(game_room_id: str, user_id: str, tool_context: ToolContext):
    """
    handle start game request by host of the game
    Args:
        game_room_id: a game room id to start the game
        user_id : user id of the player requesting to start the game
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }

    # convert to pydantic model
    game_room = GameRoom.model_validate(game_room_dict)

    # check if user is enrolled in the game
    if user_id not in game_room.players:
        return {
            "status" : "error",
            "message" : f"user is not enrolled with game room: {game_room_id}"
        }

    # check if requesting user is host, or if number of players in reached max
    if user_id != game_room.host_user_id and len(game_room.players) < game_room.max_number_players:
        return {
            "status" : "error",
            "message" : "cannot start game, still waiting for players, only host can start early"
        }

    # start the game
    game_room.game_status = "in-game"

    # save the game room state
    # TODO: replace this from "app:" scope to DB store
    state[f"{State.APP_PREFIX}{game_room.game_room_id}_{StateVariables.GAME_DETAILS}"] = game_room.model_dump()

    # following memory updates should be take care by the agent itself as needed
    # # also add to current session state (session scope) to use with prompts
    # state[StateVariables.GAME_DETAILS] = game_room.model_dump()

    # transfer to parent agent
    tool_context.actions.transfer_to_agent = tool_context._invocation_context.agent.parent_agent.name

    # return the game room details, agent will memorize as needed
    return {
        "status" : "success",
        "game_room": game_room
    }

def get_game_details(game_room_id: str, tool_context: ToolContext):
    """
    get details of the current game
    Args:
        game_room_id: a game room id to fetch details
        tool_context: The ADK tool context.
    Returns:
        A status message from getting game details
    """
    # TODO: remove this when move from "app:" scope to DB store
    state = tool_context.state

    # check if game room exists (app scope)
    # TODO: replace this from "app:" scope to DB store
    game_room_dict = state.get(f"{State.APP_PREFIX}{game_room_id}_{StateVariables.GAME_DETAILS}", None)
    if not game_room_dict:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }
    # return dtails of the game
    return {
        "status" : "success",
        "game_room" : game_room_dict
    }
