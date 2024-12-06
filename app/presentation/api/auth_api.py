from app.infrastructure.database import get_db, get_mongo
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.utils.schemas.user_schema import RegisterUserSchemaIn
from app.utils.schemas.activate_email_schema import ActivateEmailSchemaIn, ValidateEmail
from app.infrastructure.repositories.user.user_repository_postgres import UserRepositoryPostgres
from app.infrastructure.repositories.user.user_repository_mongo import UserRepositoryMongo
from app.utils.data_transfer.dtos.user.register_user_dto import RegisterUserDTO, UserAuthDTO, RegisterUserMongoDTO
from app.utils.data_transfer.dtos.user.activate_email_dto import ActivateEmailDTO
from app.application.services.auth.auth_service import AuthService
from app.application.services.email.email_smtp import EmailService
from app.utils.data_transfer.dtos.user.auth import AuthDTO
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.schemas.params_register_schema import ParamsRegisterSchemaOut
from datetime import timedelta
import os
from pathlib import Path


class AuthApi:

    @staticmethod
    async def register_user(register_user_schema: RegisterUserSchemaIn, db_postgres: Session = Depends(get_db),
                            db_mongo=Depends(get_mongo), email_service: EmailService = Depends()):

        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)

        auth_service = AuthService(postgres_repo, mongo_repo)

        try:
            register_user_dto = RegisterUserDTO(
                first_name=register_user_schema.first_name,
                second_name=register_user_schema.second_name,
                first_last_name=register_user_schema.first_last_name,
                second_last_name=register_user_schema.second_last_name,
                cell_phone=register_user_schema.cell_phone,
                date_of_birth=register_user_schema.date_of_birth,
                email=register_user_schema.email,
                gender_id=register_user_schema.gender_id,
                municipality_id=register_user_schema.municipality_id,
            )

            user = await auth_service.create_user_postgres(register_user_dto)

            user_auth_dto = UserAuthDTO(
                user_id=user.id,
                password=register_user_schema.password
            )

            auth = await auth_service.add_auth_user_postgres(user_auth_dto)

            user_mongo_dto = RegisterUserMongoDTO(
                user=user.id,
                img=register_user_schema.img
            )

            user_mongo = await auth_service.create_user_mongo(user_mongo_dto)

            await email_service.send_email(subject="Activar Cuenta", recipients=[register_user_schema.email],
                                           activation_code=auth.activation_code, name_user=user.first_name)

            return {"Registro exitoso"}

        except Exception as e:
            exc = str(e).split(': ')
            raise HTTPException(status_code=int(exc[0]), detail=exc[1])

    @staticmethod
    async def validate_user(email: ValidateEmail = Depends(), db_postgres: Session = Depends(get_db),
                            db_mongo=Depends(get_mongo)):

        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)
        auth_service = AuthService(postgres_repo, mongo_repo)
        validate_user = await auth_service.get_user_by_email_postgres(email.email)
        if validate_user is None:
            raise HTTPException(status_code=409, detail="Cuenta no encontrado")
        elif validate_user.is_activated is True:
            raise HTTPException(status_code=409, detail="La cuenta ya se encuentra activada con anterioridad")
        return {"message": f"email: {validate_user}"}

    @staticmethod
    async def activate_email(activate_email_schema: ActivateEmailSchemaIn, db_postgres: Session = Depends(get_db),
                             db_mongo=Depends(get_mongo)):

        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)
        auth_service = AuthService(postgres_repo, mongo_repo)
        validate_email = await auth_service.get_user_by_email_postgres(activate_email_schema.email)
        if validate_email is None:
            raise HTTPException(status_code=409, detail="Cuenta no encontrado")
        elif validate_email.is_activated is True:
            raise HTTPException(status_code=409, detail="La cuenta ya se encuentra activada con anterioridad")
        activation_email_dto = ActivateEmailDTO(
            email=activate_email_schema.email,
            activation_code=activate_email_schema.activation_code
        )
        activate_email = await auth_service.activate_user_postgres(activation_email_dto)
        if activate_email is None:
            raise HTTPException(status_code=409, detail="Código de activación icorrecto")
        return {"message": f"User {activate_email}"}

    @staticmethod
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                     db_postgres: Session = Depends(get_db),
                                     db_mongo=Depends(get_mongo)):

        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)
        auth_service = AuthService(postgres_repo, mongo_repo)
        auth_dto = AuthDTO(
            email=form_data.username,
            password=form_data.password
        )
        return await auth_service.login_for_access_token(auth_dto)

    @staticmethod
    async def refresh_access_token(refresh_token: str):
        pass

    @staticmethod
    async def get_params_register(db_postgres: Session = Depends(get_db), db_mongo=Depends(get_mongo)):
        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)
        auth_service = AuthService(postgres_repo, mongo_repo)
        departments = await auth_service.get_departments()
        genders = await auth_service.get_genders()
        params = ParamsRegisterSchemaOut(
            departments=departments,
            genders=genders
        )
        return params

    @staticmethod
    async def get_municipalities(id_department: int, db_postgres: Session = Depends(get_db),
                                 db_mongo=Depends(get_mongo)):
        postgres_repo = UserRepositoryPostgres(db_postgres)
        mongo_repo = UserRepositoryMongo(db_mongo)
        auth_service = AuthService(postgres_repo, mongo_repo)
        return await auth_service.get_municipalities(id_department)

    @staticmethod
    async def map_mateo(request: Request):
        from fastapi.templating import Jinja2Templates
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        TEMPLATES_DIR = BASE_DIR / "templates"
        print(TEMPLATES_DIR)
        templates = Jinja2Templates(directory=TEMPLATES_DIR)
        return templates.TemplateResponse("meteoblue/mapaMateo.html", {"request": request})


