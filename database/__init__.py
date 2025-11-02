from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('mysql+mysqlconnector://root@localhost:3306/db_biblioteca_2m')
session = Session(bind=engine)