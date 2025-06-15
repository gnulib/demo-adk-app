from pydantic import BaseModel, Field
from typing import List, Dict, Any

class GameRoom(BaseModel):
    game_room_id: str = Field(..., description="game room id")
    max_number_players: int = Field(..., description="maximum number of players that can join the game (including host)")
    host_user_id: str = Field(..., description="user id of the host for this game")
    players: List[str] = Field(default_factory=list, description="list of user ids for players enrolled in the game")
    game_status: str = Field(..., description="current status of the game (pre-game, in-game, betting, playing, post-game)")
    current_turn_player_id: str = Field(..., description="user id of the current turn player in game")
    deck: Dict[str, Any] = Field(..., description="deck of card used in the game")
    bets: Dict[str, int] = Field(..., description="player bets with player_id as key and their bet as value")
    dealer_score: int = Field(..., description="dealer's score")
    player_scores: Dict[str, int] = Field(..., description="player scores with player_id as key and their score as value")