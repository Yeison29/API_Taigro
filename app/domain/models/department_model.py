from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from ..models import *
import os
from app.domain.models.country_model import Country

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class Department(Base):
    __tablename__ = 'department'
    __table_args__ = {'schema': DB_SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey(DB_SCHEMA+'.country.id'), nullable=False)
    country = relationship(Country, backref='department')

    def __repr__(self):
        return f"Department(id={self.id}, name='{self.name}')"
