from pydantic import BaseModel, Field
from typing import List

class GameRoom(BaseModel):
    game_room_id: str = Field(..., description="game room id")
    max_number_players: int = Field(..., description="maximum number of players that can join the game (including host)")
    host_user_id: str = Field(..., description="user id of the host for this game")
    players: list[str] = Field(default_factory=list, description="list of user ids for players enrolled in the game")
    game_status: str = Field(..., description="current status of the game (pre-game, in-game, post-game)")
    current_turn_player_id: str = Field(..., description="user id of the current turn player in game")