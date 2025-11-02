import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')
if DATABASE_URI is None:
    raise RuntimeError('DATABASE_URI não foi definida')

engine = create_engine(DATABASE_URI)
session = Session(bind=engine)