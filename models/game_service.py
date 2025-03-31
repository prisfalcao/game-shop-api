from sqlalchemy import Column, String, Integer, Date, Float, UniqueConstraint
from datetime import date
from models.base import Base
from models.db import Session
from sqlalchemy.exc import IntegrityError
from models.error import GameNotFoundError, GameAlreadyExistsError, DatabaseError, NoGamesFoundError

class Game(Base):
    __tablename__ = 'Pinti_Game_Store'
    __table_args__ = (
    UniqueConstraint('name', 'platform', name='_unique_game_platform'),
)

    game_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    release = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    def __init__(self, name: str, platform: str, release: date, price: float, stock: int):
        self.name = name
        self.platform = platform
        self.release = release
        self.price = price
        self.stock = stock

def add_game(name: str, platform: str, release: date, price: float, stock: int):
    """Adds a new game to the database"""
    session = Session()
    try:
        game = Game(name, platform, release, price, stock)
        session.add(game)
        session.commit()
        session.refresh(game)
        return game
    
    except IntegrityError:
        raise GameAlreadyExistsError()
    except Exception as e:
        raise DatabaseError(f"Unable to save the new game: {str(e)}")
    finally:
        session.close()

def update_game(game_id: int, **kwargs):
    session = Session()
    try:
        game = session.query(Game).filter_by(game_id=game_id).first()
        if not game:
            raise GameNotFoundError()

        for key, value in kwargs.items():
            if hasattr(game, key):
                setattr(game, key, value)

        session.commit()
        session.refresh(game)
        return game
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