from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from models.game_service import game_list, add_game, delete_game, update_game
from schemas.game_schema import GameSchema, GameViewSchema, GameListSchema, GameDeleteWithTokenSchema, GameDeleteResponseSchema, game_presented, games_presented, AdminTokenSchema, GameTokenSchema
from models.error import GameNotFoundError, GameAlreadyExistsError, DatabaseError, NoGamesFoundError
from schemas.error import ErrorSchema
from flask_cors import CORS
from models.db import create_tables
from models.logger import logger
import json, os, requests, random
from pydantic import BaseModel
from datetime import datetime, date

info = Info(title="Game Shop API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

create_tables()

home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc or RapiDoc")
game_tag = Tag(name="Game", description="Add, view, edit and delete games from the store")

with open(os.path.join(os.path.dirname(__file__), 'appsettings.json')) as config_file:
    config = json.load(config_file)

RAWG_API_KEY = config["Rawg_Url"]["ApiKey"]
RAWG_URL = config["Rawg_Url"]["Url"]
ADMIN_TOKEN = config["Rawg_Url"]["AdminToken"]

@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, a page that allows choosing the documentation style."""
    return redirect('/openapi')

@app.post('/admin/import-games', tags=[game_tag],
          responses={"200": GameListSchema, "401": ErrorSchema, "500": ErrorSchema})
def import_games(form: AdminTokenSchema):
    """Fetches games from RAWG API, adds price and stock, and saves them to the store database.

    Requires a valid admin token in the request body."""

    if form.token != ADMIN_TOKEN:
        logger.warning("Unauthorized attempt to import games.")
        return {"error": "Unauthorized. Invalid admin token."}, 401

    logger.info("Fetching games from RAWG API...")

    try:
        response = requests.get(f"{RAWG_URL}?key={RAWG_API_KEY}&page_size=12")
        response.raise_for_status()
        games_data = response.json()["results"]

        imported_games = []
        for rawg_game in games_data:
            name = rawg_game["name"]
            release = rawg_game.get("released")
            try:
                release = datetime.strptime(release, "%Y-%m-%d").date() if release else date.today()
            except ValueError:
                release = date.today()
            platforms = rawg_game.get("platforms", [])
            platform_names = [p["platform"]["name"] for p in platforms]
            platform = ", ".join(platform_names) if platform_names else "Unknown"

            price = round(random.uniform(99.0, 499.0), 2)
            stock = random.randint(5, 50)

            try:
                game = add_game(name, platform, release, price, stock)
                imported_games.append(game)
            except GameAlreadyExistsError:
                logger.info(f"Skipped: Game '{name}' already exists on platform(s): {platform}")

        logger.info(f"{len(imported_games)} games imported with success.")
        return games_presented(imported_games), 200

    except requests.RequestException as e:
        logger.error(f"Error fetching from RAWG API: {str(e)}")
        return {"error": "Failed to fetch data from RAWG API"}, 500
    except Exception as e:
        logger.error(f"Unexpected error during game import: {str(e)}")
        return {"error": "Unexpected error occurred while importing games."}, 500

@app.post('/game', tags=[game_tag],
          responses={"200": GameViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_new_game(form: GameSchema):
    """Adds a new game to the store.

    Returns a representation of the created game."""
    logger.info(f"[INFO] Received request to add new game: {form.name} - {form.platform}")

    try:
        new_game = add_game(form.name, form.platform, form.release, form.price, form.stock)
        logger.info(f"Game added successfully: {new_game.game_id} - {new_game.name}")
        return game_presented(new_game), 200
    except GameAlreadyExistsError as e:
        logger.warning(f"Game already exists: {form.name}")
        return {"error": e.message}, e.status_code
    except DatabaseError as e:
        logger.error(f"Database error while adding game: {e.message}")
        return {"error": e.message}, e.status_code

@app.get('/games', tags=[game_tag],
         responses={"200": GameListSchema, "404": ErrorSchema})
def list_games():
    """Gets the list of all the games registered in the store.

    Returns a list of games.
    """
    games = game_list()
    try:
        return games_presented(games), 200
    except NoGamesFoundError as e:
        logger.error(f"No games in the list: {e.message}")
        return {"error": e.message}, e.status_code

@app.put('/game', tags=[game_tag],
         responses={"200": GameViewSchema, "401": ErrorSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_game_route(form: GameTokenSchema):
    """
    Updates the details of an existing game in the store. Requires an admin token.

    - **token**: Admin access token.
    - **game_id**: ID of the game to update.
    - **Fields**: Price and stock."""
    if form.token != ADMIN_TOKEN:
        logger.warning("Unauthorized attempt to update game.")
        return {"error": "Unauthorized. Invalid admin token."}, 401

    logger.info(f"Received request to update game {form.game_id} with fields: {form.model_dump(exclude_unset=True)}")
    try:
        updated_game = update_game(
            form.game_id,
            **form.model_dump(exclude={"game_id", "token"}, exclude_unset=True)
        )
        logger.info(f"Game with id {form.game_id} updated successfully.")
        return game_presented(updated_game), 200
    except GameNotFoundError as e:
        logger.error(f"Cannot update - game not found: {e.message}")
        return {"error": e.message}, e.status_code
    except DatabaseError as e:
        logger.error(f"Database error while updating game: {e.message}")
        return {"error": e.message}, e.status_code

@app.delete('/game', tags=[game_tag],
            responses={"200": GameDeleteResponseSchema, "404": ErrorSchema, "401": ErrorSchema})
def remove_game(form: GameDeleteWithTokenSchema):
    """Removes a game from the store. Requires admin token.

    Returns a confirmation message upon removal."""
    if form.token != ADMIN_TOKEN:
        logger.warning("Unauthorized delete attempt.")
        return {"error": "Unauthorized. Invalid admin token."}, 401
    try:
        delete_game(form.game_id)
        logger.info(f"Game with id {form.game_id} was removed successfully from the store.")
        return {"message": "Game removed successfully from the store", "game_id": form.game_id}, 200
    except GameNotFoundError as e:
        logger.error(f"Game not found to be deleted: {e.message}")
        return {"error": e.message}, e.status_code