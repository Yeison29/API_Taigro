from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from ..models import *
import os
from app.domain.models.municipality import Municipality
from app.domain.models.gender_model import Gender

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': DB_SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=True)
    first_last_name = Column(String(50), nullable=False)
    second_last_name = Column(String(50), nullable=True)
    cell_phone = Column(String(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    municipality_id = Column(Integer, ForeignKey(DB_SCHEMA+'.municipality.id'), nullable=False)
    municipality = relationship(Municipality, backref='users')
    gender_id = Column(String(10), ForeignKey(DB_SCHEMA + '.gender.code'), nullable=False)
    gender = relationship(Gender, backref='users')

    def __repr__(self):
        full_name = f"{self.first_name} "

        if self.second_name:
            full_name += f"{self.second_name} "

        full_name += f"{self.first_last_name} "

        if self.second_last_name:
            full_name += f"{self.second_last_name}"

        return f"User(id={self.id}, email='{self.email}', name='{full_name.strip()}')"
