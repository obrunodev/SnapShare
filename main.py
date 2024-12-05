from fastapi import FastAPI

from sqlalchemy import create_engine, MetaData, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from databases import Database

app = FastAPI()

DATABASE_URL = "sqlite:///./database.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=True)

metadata = MetaData()
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    text = Column(String)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.on_event("startup")
def startup():
    database.connect()

@app.on_event("shutdown")
def shutdown():
    database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
