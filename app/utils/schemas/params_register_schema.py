import re
from pydantic import Field, BaseModel, field_validator, EmailStr
from datetime import date
from typing import Optional, List


class DepartmentsSchemaOut(BaseModel):
    name: str = Field(...)
    id: int = Field(...)
    country_id: int = Field(...)

    class Config:
        from_attributes = True


class GendersSchemaOut(BaseModel):
    name: str = Field(...)
    code: str = Field(...)

    class Config:
        from_attributes = True


class ParamsRegisterSchemaOut(BaseModel):
    departments: List[DepartmentsSchemaOut] = Field(...)
    genders: List[GendersSchemaOut] = Field(...)


class MunicipalitiesSchemaOut(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

    class Config:
        from_attributes = True
