""" constants to use with state / memory of agents """

class StateVariables():
    IS_INITIALIZED = False
    GAME_DETAILS = "game_details"
    USER_DETAILS = "user_details"
    USER_ID = "user_id"
    USER_ROLE = "user_role"
    GAME_ROOM_ID = "game_room_id"
    CURRENT_GAME = "current_game"

class GAME_DETAILS():
    GAME_ROOM_ID = StateVariables.GAME_ROOM_ID
    CURRENT_TURN_PLAYER_ID = "current_turn_player_id"
    PLAYERS = "players"
    HOST_USER_ID = "host_user_id"
    MAX_NUMBER_PLAYERS = "max_number_players"
    GAME_STATUS = "game_status"
