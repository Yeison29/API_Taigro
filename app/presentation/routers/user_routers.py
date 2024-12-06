from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.presentation.api.auth_api import AuthApi


class UserRouter(APIRouter):

    def __init__(self):
        super().__init__()
        self.router = APIRouter()
        self._setup_routes()

    def _setup_routes(self):
        self.router.post("/token", status_code=200, tags=['Token'])(AuthApi.login_for_access_token)
        self.router.post("/refresh_token", status_code=200, tags=['Token'])(AuthApi.refresh_access_token)
        self.router.post("/registerUser", status_code=200, tags=['Auth'])(AuthApi.register_user)
        self.router.get("/validateUser", status_code=200, tags=['Auth'])(AuthApi.validate_user)
        self.router.put("/activateEmail", status_code=200, tags=['Auth'])(AuthApi.activate_email)
        self.router.get("/getParamsRegister", status_code=200, tags=['Auth'])(AuthApi.get_params_register)
        self.router.get("/getMunicipalities", status_code=200, tags=['Auth'])(AuthApi.get_municipalities)
        self.router.get("/mapMateo", status_code=200, response_class=HTMLResponse, tags=['Mapas'])(AuthApi.map_mateo)

