""" constants to use with state / memory of agents """

class StateVariables():
    IS_INITIALIZED = False
    GAME_DETAILS = "game_details"
    USER_DETAILS = "user_details"
    USER_ID = "user_id"
    USER_BET = "user_bet"
    USER_PURSE = "user_purse"
    USER_ROLE = "user_role"
    GAME_ROOM_ID = "game_room_id"
    CURRENT_GAME = "current_game"
    LAST_USER_MESSAGE = "_last_user_message"

class GAME_DETAILS():
    GAME_ROOM_ID = StateVariables.GAME_ROOM_ID
    CURRENT_TURN_PLAYER_ID = "current_turn_player_id"
    PLAYERS = "players"
    HOST_USER_ID = "host_user_id"
    MAX_NUMBER_PLAYERS = "max_number_players"
    GAME_STATUS = "game_status"

class Models:
    REASONING_MODEL="gemini-2.5-pro-preview-05-06"
    FLASH_MODEL="gemini-2.5-flash-preview-05-20"
    ECO_MODEL="gemini-2.5-flash-preview-05-20"
