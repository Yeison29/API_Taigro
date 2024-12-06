from fastapi import FastAPI
from app.presentation.routers.user_routers import UserRouter
from app.infrastructure.database.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware

user_router = UserRouter()


class App:
    def __init__(self):
        self.app = FastAPI()
        self.configure()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["*"],
        )

    def configure(self):
        init_db()
        self.app.include_router(user_router.router)


app = App()
