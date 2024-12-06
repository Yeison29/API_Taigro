from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
from ..models import *
import os

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class Gender(Base):
    __tablename__ = 'gender'
    __table_args__ = {'schema': DB_SCHEMA}

    name = Column(String(50), nullable=False, unique=False)
    code = Column(String(10), nullable=False, unique=True, primary_key=True)

    def __repr__(self):
        return f"Gender(name='{self.name}', code='{self.code})"
