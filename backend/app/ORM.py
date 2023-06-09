from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db

db_user = "joro"
db_pwd = "34092109"
db_host = "postgreSQL"
db_port = 5432
db_name = "linkscribe"

SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

