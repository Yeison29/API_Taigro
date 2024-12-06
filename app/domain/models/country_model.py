from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
from ..models import *
import os

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = {'schema': DB_SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Country(id={self.id}, name='{self.name}')"
