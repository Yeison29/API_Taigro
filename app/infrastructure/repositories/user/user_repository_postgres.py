from app.domain.models.user_model import User
from app.domain.models.auth_model import Auth
from app.utils.data_transfer.dtos.user.register_user_dto import RegisterUserDTO, AddUserAuthDTO
from app.utils.data_transfer.dtos.user.activate_email_dto import ActivateEmailDTO
from app.utils.data_transfer.dtos.user.auth import AuthDTO
from app.domain.models.department_model import Department
from app.domain.models.gender_model import Gender
from app.domain.models.municipality import Municipality
from fastapi import HTTPException
from sqlalchemy.orm import joinedload


class UserRepositoryPostgres:
    def __init__(self, db_session):
        self.db_session = db_session

    async def get_user_by_email(self, email: str):
        return (self.db_session.query(Auth.is_activated, Auth.fch_register, User).join(User, Auth.user_id == User.id)
                .filter(User.email == email)
                .first())

    async def create_user(self, user_data: RegisterUserDTO):
        validate_email = await UserRepositoryPostgres.get_user_by_email(self, user_data.email)
        if validate_email:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

        new_user = User(**user_data.__dict__)
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user

    async def add_aunt(self, aunt_data: AddUserAuthDTO):
        new_auth = Auth(**aunt_data.__dict__)
        self.db_session.add(new_auth)
        self.db_session.commit()
        self.db_session.refresh(new_auth)
        return new_auth

    async def activate_user(self, email_data: ActivateEmailDTO):
        auth = (self.db_session.query(Auth)
                .join(User, Auth.user_id == User.id)
                .filter(User.email == email_data.email, Auth.activation_code == email_data.activation_code)
                .first())

        if auth:
            auth.is_activated = True
            self.db_session.commit()

        return (self.db_session.query(Auth.is_activated, Auth.fch_register, User).join(User, Auth.user_id == User.id)
                .filter(User.email == email_data.email, Auth.activation_code == email_data.activation_code)
                .first())

    async def authenticaion_user(self, email: str):
        return (
            self.db_session.query(Auth.is_activated, Auth.password, Auth.fch_register, User)
            .join(User, Auth.user_id == User.id)
            .filter(User.email == email)
            .first())

    async def get_departments(self):
        return self.db_session.query(Department).all()

    async def get_genders(self):
        return self.db_session.query(Gender).all()

    async def get_municipalities(self, id_department: int):
        return self.db_session.query(Municipality.id, Municipality.name).filter(
            Municipality.department_id == id_department).all()
