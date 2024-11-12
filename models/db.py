from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from models.base import Base

db_path = "database/"
if not os.path.exists(db_path):
   os.makedirs(db_path)

db_url = f'sqlite:///{db_path}/database.db'

engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url) 

def create_tables():
    Base.metadata.create_all(engine)