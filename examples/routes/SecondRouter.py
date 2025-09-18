from py_micro_services.core import PyMicroserviceRouter, get, auth
from fastapi import Request

class SecondRouter(PyMicroserviceRouter):
    @get("/ping")
    async def ping(self) -> str:
        return "second router - pong"
    
    @auth(["admin"])
    @get("/adminping")
    async def admin_ping(self, request: Request) -> str:
        print("Authenticated user ID:", self.user_id, " - roles: ", self.user_roles)
        return "second router - admin pong"
