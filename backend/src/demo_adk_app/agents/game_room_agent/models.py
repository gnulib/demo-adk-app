from pydantic import BaseModel, Field
from typing import List, Dict, Any

class GameRoom(BaseModel):
    game_room_id: str = Field(None, description="game room id")
    max_number_players: int = Field(1, description="maximum number of players that can join the game (including host)")
    host_user_id: str = Field(None, description="user id of the host for this game")
    players: List[str] = Field([], description="list of user ids for players enrolled in the game")
    game_status: str = Field(None, description="current status of the game (pre-game, in-game, betting, playing, post-game)")
    current_turn_player_id: str = Field(None, description="user id of the current turn player in game")
    deck: Dict[str, Any] = Field({}, description="deck of card used in the game")
    bets: Dict[str, int] = Field({}, description="player bets with player_id as key and their bet as value")
    dealer_score: int = Field(0, description="dealer's score")
    player_scores: Dict[str, int] = Field({}, description="player scores with player_id as key and their score as value")