from py_micro_services.core import PyMicroserviceRouter, get

class SecondRouter(PyMicroserviceRouter):
    @get("/ping")
    async def ping(self) -> str:
        return "second router - pong"
    
