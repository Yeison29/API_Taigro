import re
from pydantic import Field, BaseModel, field_validator, EmailStr
from datetime import date
from typing import Optional


class ValidateEmail(BaseModel):
    email: EmailStr = Field(...)


class ActivateEmailSchemaIn(ValidateEmail):
    activation_code: str = Field(...)

    @field_validator('activation_code')
    @classmethod
    def check_activation_code_length(cls, v):
        if v is None or v == "":
            raise ValueError('El código de activación es obligatoria')
        elif len(v) < 12:
            raise ValueError('El código de activación no puede tener menos de 12 caracteres')
        elif len(v) > 12:
            raise ValueError('El código de activación no puede tener más de 12 caracteres')
        return v
