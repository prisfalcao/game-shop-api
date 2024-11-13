from pydantic import BaseModel
from typing import List
from datetime import date
from models.game_service import Game

class GameSchema(BaseModel):
    """Defines the structure for data needed to add a new game to the collection."""
    name: str
    platform: str
    release_date: date
    developer: str
    condition: str

class GameViewSchema(BaseModel):
    """Defines how a single game will be returned for detailed view."""
    game_id: int
    name: str
    platform: str
    release_date: date
    developer: str
    condition: str

class GameListSchema(BaseModel):
    """Defines how a list of games will be returned."""
    games: List[GameViewSchema]

def games_presented(games: List[Game]):
    """Returns a representation of games following the schema defined in GameListSchema."""
    result = []
    for game in games:
        result.append({
            "game_id": game.game_id,
            "name": game.name,
            "platform": game.platform,
            "release_date": game.release_date,
            "developer": game.developer,
            "condition": game.condition,
        })
    return {"games": result}

class GameDeleteSchema(BaseModel):
    """Defines the structure of the data returned after a delete request."""
    game_id: int

def game_presented(game: Game):
    """Returns a representation of a single game following the schema defined in GameViewSchema."""
    return {
        "game_id": game.game_id,
        "name": game.name,
        "platform": game.platform,
        "release_date": game.release_date,
        "developer": game.developer,
        "condition": game.condition,
    }
