from sqlmodel import SQLModel
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://rootusers:rootroot@db:5432/managers"

BASE = SQLModel

engine = create_engine(DATABASE_URL, echo=True)