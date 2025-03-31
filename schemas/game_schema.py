from pydantic import BaseModel
from typing import List
from datetime import date
from models.game_service import Game

class GameSchema(BaseModel):
    """Defines the structure for data needed to add a new game to the collection."""
    name: str
    platform: str
    release: date = "2025-03-18"
    price: float
    stock: int

class GameViewSchema(BaseModel):
    """Defines how a single game will be returned for detailed view."""
    game_id: int
    name: str
    platform: str
    release: date
    price: float
    stock: int

class GameUpdateSchema(BaseModel):
    game_id: int
    price: float
    stock: int

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
            "release": game.release,
            "price": game.price,
            "stock": game.stock
        })
    return {"games": result}

class GameDeleteWithTokenSchema(BaseModel):
    """Schema to receive the game_id and token for deletion."""
    game_id: int
    token: str

class GameDeleteResponseSchema(BaseModel):
    """Schema for the response after successfully deleting a game."""
    message: str
    game_id: int  

class GameDeleteSchema(BaseModel):
    """Defines the structure of the data returned after a delete request."""
    game_id: int
    token: str = "test-token"

def game_presented(game: Game):
    """Returns a representation of a single game following the schema defined in GameViewSchema."""
    return {
        "game_id": game.game_id,
        "name": game.name,
        "platform": game.platform,
        "release": game.release,
        "price": game.price,
        "stock": game.stock
    }

class AdminTokenSchema(BaseModel):
    """Requests a token to allow the import of a game list from RAWG API."""
    token: str = "test-token"

class GameTokenSchema(GameUpdateSchema):
    """Requests a token to allow the update of price and stock of a game."""
    token: str = "test-token"