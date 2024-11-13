from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from models.game_service import Game
from models.db import Session
from schemas.game_schema import GameSchema, GameViewSchema, GameListSchema, GameDeleteSchema, game_presented, games_presented
from schemas.error import ErrorSchema
from flask_cors import CORS
import json

info = Info(title="Game Collection API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc or RapiDoc")
game_tag = Tag(name="Game", description="Add, view, and delete games from the collection")

@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, a page that allows choosing the documentation style.
    """
    return redirect('/openapi')

@app.post('/game', tags=[game_tag],
          responses={"200": GameViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_game(form: GameSchema):
    """Adds a new game to the collection

    Returns a representation of the created game.
    """
    new_game = Game(
        name=form.name,
        platform=form.platform,
        release_date=form.release_date,
        developer=form.developer,
        condition=form.condition
    )

    try:
        session = Session()
        session.add(new_game)
        session.commit()
        return game_presented(new_game), 200

    except IntegrityError:
        error_msg = "A game with the same name already exists in the database."
        return {"message": error_msg}, 409

    except Exception:
        error_msg = "Unable to save the new game."
        return {"message": error_msg}, 400

@app.get('/games', tags=[game_tag],
         responses={"200": GameListSchema, "404": ErrorSchema})
def game_list():
    """Fetches all games registered in the collection

    Returns a list of games.
    """
    session = Session()
    games = session.query(Game).all()

    if not games:
        return {"games": []}, 200
    else:
        return games_presented(games), 200

@app.delete('/game', tags=[game_tag],
            responses={"200": GameDeleteSchema, "404": ErrorSchema})
def delete_game(query: GameDeleteSchema):
    """Deletes a game based on the provided ID

    Returns a confirmation message upon removal.
    """
    game_id = query.game_id
    session = Session()
    count = session.query(Game).filter(Game.game_id == game_id).delete()
    session.commit()

    if count:
        return {"message": "Game removed", "game_id": game_id}, 200
    else:
        error_msg = "Game not found in the database."
        return {"message": error_msg}, 404
