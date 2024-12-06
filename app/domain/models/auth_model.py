from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from ..models import *
import os
from app.domain.models.user_model import User

load_dotenv()
DB_SCHEMA = os.getenv("DB_SCHEMA")


class Auth(Base):
    __tablename__ = 'auth'
    __table_args__ = {'schema': DB_SCHEMA}

    user_id = Column(Integer, ForeignKey(DB_SCHEMA+'.users.id'), primary_key=True)
    user = relationship(User, backref='auth')
    activation_code = Column(String(12), nullable=False)
    is_activated = Column(Boolean, default=False, nullable=False)
    password = Column(String(60), nullable=False)
    fch_register = Column(Date, nullable=False)

    def __repr__(self):
        return (f"user_id={self.user_id}, activation_code='{self.activation_code}', "
                f"is_activated={self.is_activated}")
