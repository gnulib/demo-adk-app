from google.adk.tools import ToolContext

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
    user_id = state.get("user_id", None)
    if not user_id:
        return {
            "status" : "error",
            "message" : "user id is not known"
        }
    # create a new game room
    new_game_room_id = "1234" # todo: change with actual new id generation later
    state["game_room_id"] = new_game_room_id
    # make the user as host of the game
    state["user_role"] = "host"
    # add user to player list of the game room (application scope, to share with all users)
    state[f"app:{new_game_room_id}_players"] = [user_id]
    # add number if players for game (application scope, to share with all users)
    state[f"app:{new_game_room_id}_num_players"] = max_num_players
    return {
        "status" : "success",
        "message" : f"created new game room with ID {new_game_room_id} for maximum {max_num_players} players"
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
    user_id = state.get("user_id", None)
    if not user_id:
        return {
            "status" : "error",
            "message" : "user id is not known"
        }
    # check if game room exists (app scope)
    max_num_players = state.get(f"app:{game_room_id}_num_players", 0)
    players = state.get(f"app:{game_room_id}_players", None)
    if not players:
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} does not exist"
        }
    # check if game has room for new player to join
    if max_num_players >= len(players):
        return {
            "status" : "error",
            "message" : f"game room with id {game_room_id} has already reached max players"
        }
    # set the game room for current session
    state["game_room_id"] = game_room_id
    # make the user as player of the game
    state["user_role"] = "player"
    # add user to player list of the game room (application scope, to share with all users)
    players.append(user_id)
    state[f"app:{game_room_id}_players"] = players
    return {
        "status" : "success",
        "message" : f"added user as player for game room with ID {game_room_id}"
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

def get_game_status(tool_context: ToolContext):
    """
    get status of the current game
    Args:
        tool_context: The ADK tool context.
    Returns:
        A status message from handling user request
    """
    state = tool_context.state
