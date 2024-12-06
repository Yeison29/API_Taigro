from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from ..models import *
import os
from app.domain.models.department_model import Department

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class Municipality(Base):
    __tablename__ = 'municipality'
    __table_args__ = {'schema': DB_SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=False)
    department_id = Column(Integer, ForeignKey(DB_SCHEMA+'.department.id'), nullable=False)
    department = relationship(Department, backref='municipality')

    def __repr__(self):
        return f"Municipality(id={self.id}, name='{self.name}')"
