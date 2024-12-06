from app.utils.data_transfer.dtos.user.register_user_dto import RegisterUserDTO, UserAuthDTO, AddUserAuthDTO, \
    RegisterUserMongoDTO
from fastapi import HTTPException, status
from app.utils.data_transfer.dtos.user.activate_email_dto import ActivateEmailDTO
from app.utils.hash.hash_bcrypt import hash_password, check_password
from app.utils.generete_code.generate_activation_code import generate_random_code
from app.application.services.jwt.jwt import create_access_token, create_refresh_token, verify_token
from app.utils.data_transfer.dtos.user.auth import AuthDTO
from app.utils.schemas.params_register_schema import DepartmentsSchemaOut, GendersSchemaOut, MunicipalitiesSchemaOut
from datetime import datetime


class AuthService:
    def __init__(self, postgres_repository, mongo_repository):
        self.postgres_repository = postgres_repository
        self.mongo_repository = mongo_repository

    async def create_user_postgres(self, user_data: RegisterUserDTO):
        return await self.postgres_repository.create_user(user_data)

    async def add_auth_user_postgres(self, auth_data: UserAuthDTO):
        password_hash = await hash_password(auth_data.password)
        code_activation = await generate_random_code(12)
        user_auth = AddUserAuthDTO(
            user_id=auth_data.user_id,
            password=password_hash,
            activation_code=code_activation,
            fch_register=datetime.now().date(),
            is_activated=False)
        return await self.postgres_repository.add_aunt(user_auth)

    async def create_user_mongo(self, user_data: RegisterUserMongoDTO):
        return await self.mongo_repository.create_user(user_data)

    async def get_user_by_email_postgres(self, email: str):
        return await self.postgres_repository.get_user_by_email(email)

    async def activate_user_postgres(self, activate_email_data: ActivateEmailDTO):
        return await self.postgres_repository.activate_user(activate_email_data)

    async def login_for_access_token(self, auth_data: AuthDTO):
        user = await self.postgres_repository.authenticaion_user(auth_data.email)



        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no se encuentra registrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif user.is_activated is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La cuenta del Usuario no esta activa",
                headers={"WWW-Authenticate": "Bearer"},
            )

        validate_password = await check_password(user.password, auth_data.password)

        if validate_password is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña Icorrrecta",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": user.User.id}
        )
        refresh_token = create_refresh_token(data={"sub": user.User.id})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    async def refresh_access_token(self, refresh_token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = verify_token(refresh_token, credentials_exception)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": payload["sub"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_departments(self):
        departments = await self.postgres_repository.get_departments()
        return [DepartmentsSchemaOut.from_orm(dept) for dept in departments]

    async def get_genders(self):
        genders = await self.postgres_repository.get_genders()
        return [GendersSchemaOut.from_orm(gender) for gender in genders]

    async def get_municipalities(self, id_department: int):
        municipalities = await self.postgres_repository.get_municipalities(id_department)
        return [MunicipalitiesSchemaOut.from_orm(municipality) for municipality in municipalities]
