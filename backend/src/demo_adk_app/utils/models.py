from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GameRoom(BaseModel):
    game_room_id: str = Field(None, description="game room id")
    max_number_players: int = Field(1, description="maximum number of players that can join the game (including host)")
    host_user_id: str = Field(None, description="user id of the host for this game")
    players: List[str] = Field([], description="list of user ids for players enrolled in the game")
    game_status: str = Field("pre-game", description="current status of the game (pre-game, in-game, betting, playing, post-game)")
    current_turn_player_id: Optional[str] = Field(None, description="user id of the current turn player in game")
    deck: Dict[str, Any] = Field({}, description="deck of card used in the game")
    cards: List[Dict[str, Any]] = Field([], description="cards in the deck used for game")
    player_cards: Dict[str, List[Any]] = Field({}, description="player cards with player_id as key and their cards as value")
    bets: Dict[str, int] = Field({}, description="player bets with player_id as key and their bet as value")
    dealer_score: int = Field(0, description="dealer's score")
    dealer_cards: List[Any] = Field([], description="dealer's cards")
    player_scores: Dict[str, int] = Field({}, description="player scores with player_id as key and their score as value")