from sqlalchemy import Column, String, Integer, Date
from datetime import date
from models.base import Base
from models.db import Session
from sqlalchemy.exc import IntegrityError
from models.error import GameNotFoundError, GameAlreadyExistsError, DatabaseError, NoGamesFoundError

class Game(Base):
    __tablename__ = 'my_game_collection'

    game_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    developer = Column(String, nullable=False)
    condition = Column(String, nullable=False)

    def __init__(self, name: str, platform: str, release_date: date, developer: str, condition: str):
        self.name = name
        self.platform = platform
        self.release_date = release_date
        self.developer = developer
        self.condition = condition

def add_game(name: str, platform: str, release_date: date, developer: str, condition: str):
    """Adds a new game to the database"""
    session = Session()
    try:
        game = Game(name, platform, release_date, developer, condition)
        session.add(game)
        session.commit()
        session.refresh(game)
        return game
    
    except IntegrityError:
        raise GameAlreadyExistsError()
    except Exception:
        raise DatabaseError("Unable to save the new game")
    finally:
        session.close()

def game_list():
    """Gets all the games listed in the database"""
    session = Session()
    try:
        games = session.query(Game).all()
        return games
    except Exception:
        raise NoGamesFoundError()
    finally:
        session.close()

def delete_game(game_id: int):
    """Removes a game from the database by its ID"""
    session = Session()
    try:
        game = session.query(Game).filter_by(game_id=game_id).first()
        if game:
            session.delete(game)
            session.commit()
            return True
        else:
            raise GameNotFoundError()
    finally:
        session.close()