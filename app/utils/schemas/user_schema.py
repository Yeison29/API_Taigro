import re
from pydantic import Field, BaseModel, field_validator, EmailStr
from datetime import date
from typing import Optional


class UserSchemaIn(BaseModel):
    first_name: str = Field(...)
    second_name: str | None = Field(None)
    first_last_name: str = Field(...)
    second_last_name: str | None = Field(None)
    cell_phone: str = Field(...)
    date_of_birth: date = Field()
    email: EmailStr = Field(...)
    municipality_id: int = Field(...)
    gender_id: str = Field(...)

    @field_validator('first_name')
    @classmethod
    def check_first_name_length(cls, v):
        if len(v) < 2:
            raise ValueError('El primer nombre debe tener al menos 2 caracteres')
        elif len(v) > 50:
            raise ValueError('El primer nombre no puede tener más de 50 caracteres')
        return v

    @field_validator('second_name')
    @classmethod
    def check_second_name_length(cls, v):
        if v is not None and isinstance(v, str) and len(v) < 2:
            raise ValueError('El segundo nombre debe tener al menos 2 caracteres')
        elif v is not None and isinstance(v, str) and len(v) > 50:
            raise ValueError('El segundo nombre no puede tener más de 50 caracteres')
        return v

    @field_validator('first_last_name')
    @classmethod
    def check_first_last_name_length(cls, v):
        if len(v) < 2:
            raise ValueError('El primer apellido debe tener al menos 2 caracteres')
        elif len(v) > 50:
            raise ValueError('El primer apellido no puede tener más de 50 caracteres')
        return v

    @field_validator('second_last_name')
    @classmethod
    def check_second_last_name_length(cls, v):
        if v is not None and isinstance(v, str) and len(v) < 2:
            raise ValueError('El segundo apellido debe tener al menos 2 caracteres')
        elif v is not None and isinstance(v, str) and len(v) > 50:
            raise ValueError('El segundo apellido no puede tener más de 50 caracteres')
        return v

    @field_validator('cell_phone')
    @classmethod
    def check_cell_phone_length(cls, v):
        if v is None or v == "":
            raise ValueError('El número de celular es obligatorio')
        elif not re.match('^[0-9]+$', v):
            raise ValueError('El número de celular solo debe contener números')
        elif len(v) < 10:
            raise ValueError('El número de celular debe tener al menos 10 dígitos')
        elif len(v) > 10:
            raise ValueError('El número de celular no puede tener más de 10 dígitos')
        return v

    @field_validator('date_of_birth')
    @classmethod
    def check_date_of_birth(cls, v):
        if v is None or v == "":
            raise ValueError('La fecha de nacimiento es obligatoria')
        if v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser futura')
        return v

    @field_validator('gender_id')
    @classmethod
    def check_gender_id(cls, v):
        if v is None or v == "":
            raise ValueError('El genero es obligatorio')
        elif len(v) < 1:
            raise ValueError('El código del genero debe tener al menos 1 caracteres')
        elif len(v) > 10:
            raise ValueError('El código del genero debe no tener más de 10 caracteres')
        return v


class UserSchemaOut(UserSchemaIn):
    id_user: int = Field(...)

    @field_validator('id_user')
    @classmethod
    def check_id_user(cls, v):
        if v is None or v == 0:
            raise ValueError('El id del usuario es obligatorio')
        elif v <= 0:
            raise ValueError('El id del usuario no puede ser cero o negativo')


class RegisterUserSchemaIn(UserSchemaIn):
    password: str = Field(...)
    img: str | None = Field(...)

    @field_validator('password')
    @classmethod
    def check_password_length(cls, v):
        if v is None or v == "":
            raise ValueError('La contraseña es obligatoria')
        elif len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        elif len(v) > 12:
            raise ValueError('La contraseña no puede tener más de 12 caracteres')
        return v


class UserSchemaOut2(UserSchemaOut):
    name_gender: str = Field(...)

    @field_validator('name_gender')
    @classmethod
    def check_name_gender(cls, v):
        if v is None or v == "":
            raise ValueError('El nombre del genero es obligatorio')
        elif len(v) < 2:
            raise ValueError('El nombre del genero debe tener al menos 2 caracteres')
        elif len(v) > 50:
            raise ValueError('El nombre del genero no debe tener más de 50 caracteres')
        return v
