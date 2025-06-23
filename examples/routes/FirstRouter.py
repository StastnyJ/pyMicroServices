from py_micro_services.core import PyMicroserviceRouter, get, post
from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: int | None = None

class FirstRouter(PyMicroserviceRouter):
    @get("/ping")
    async def ping(self) -> str:
        return "first router - pong"
    
    @get("/service_info")
    async def service_info(self) -> str:
        return "Service name: " + self._service.config.service_name

    @post("/make_user_older")
    async def make_user_older(self, user: User, years: int) -> User:
        user.age += years
        return user