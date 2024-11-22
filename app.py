from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from models.game_service import game_list, add_game, delete_game
from schemas.game_schema import GameSchema, GameViewSchema, GameListSchema, GameDeleteSchema, game_presented, games_presented
from models.error import GameNotFoundError, GameAlreadyExistsError, DatabaseError, NoGamesFoundError
from schemas.error import ErrorSchema
from flask_cors import CORS
from models.db import create_tables

info = Info(title="Game Collection API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

create_tables()

home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc or RapiDoc")
game_tag = Tag(name="Game", description="Add, view, and delete games from the collection")

@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, a page that allows choosing the documentation style.
    """
    return redirect('/openapi')

@app.post('/game', tags=[game_tag],
          responses={"200": GameViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_new_game(form: GameSchema):
    """Adds a new game to the collection

    Returns a representation of the created game.
    """
    try:
        new_game = add_game(form.name, form.platform, form.release_date, form.developer, form.condition)
        return game_presented(new_game), 200
    except GameAlreadyExistsError as e:
        return {"error": e.message}, e.status_code
    except DatabaseError as e:
        return {"error": e.message}, e.status_code

@app.get('/games', tags=[game_tag],
         responses={"200": GameListSchema, "404": ErrorSchema})
def list_games():
    """Gets the list of all the games registered in the collection

    Returns a list of games.
    """
    games = game_list()
    try:
        return games_presented(games), 200
    except NoGamesFoundError as e:
        return {"error": e.message}, e.status_code

@app.delete('/game', tags=[game_tag],
            responses={"200": GameDeleteSchema, "404": ErrorSchema})
def remove_game(query: GameDeleteSchema):
    """Removes a game from the collection, based on the provided Game ID

    Returns a confirmation message upon removal.
    """
    game_id = query.game_id
    try:
        delete_game(game_id)
        return {"message": "Game removed successfully from the collection", "game_id": game_id}, 200
    except GameNotFoundError as e:
        return {"error": e.message}, e.status_code
