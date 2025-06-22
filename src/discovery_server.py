from fastapi import FastAPI
from typing import Dict, List
from fastapi.responses import HTMLResponse
from fastapi import  Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dataclasses import dataclass
import uvicorn
import time
import random
import json

class DiscoveryServerConfig(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8880)
    debug: bool = Field(default=False)
    down_timeout: int = Field(default=60)
    clear_timeout: int = Field(default=1800)

    @classmethod
    def load(cls, path: str) -> "DiscoveryServerConfig":
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(**data)

@dataclass
class ServiceInfo:
    name: str
    active_instances: list[str]
    status: str = "active"

app = FastAPI()

config = DiscoveryServerConfig.load("config/discovery_server_config.json")
templates = Jinja2Templates(directory="templates")


# A simple service registry to register and list services
# Service name -> address mapping (IP address or hostname and last health-check timestamp)
registry: Dict[str, Dict[str, float]] = {}


@app.post("/register")
async def register(service_name: str, address: str):
    if not service_name in registry:
        registry[service_name] = {}
    registry[service_name][address] = time.time()


@app.post("/deregister")
async def deregister(service_name: str, address: str):
    if service_name in registry and address in registry[service_name]:
        del registry[service_name][address]
        if registry[service_name] == {}:
            del registry[service_name]


@app.get("/services")
async def list_services() -> List[ServiceInfo]:
    result = [ServiceInfo(name=name, active_instances=_get_active_services(name)) for name in list(registry.keys())]
    for service in result:
        service.status = "active" if service.active_instances else "inactive"
    return result


@app.get("/address")
async def get_service(service_name: str) -> str:
    instances = _get_active_services(service_name)
    if not instances or len(instances) == 0:
        return "Service has no running instances", 404
    return random.choice(instances)



@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request)-> HTMLResponse:
    return templates.TemplateResponse("discovery_server_dashboard.html", {"request": request})


@app.get("/ping")
async def ping() -> str:
    return "pong"


def _get_active_services(service_name: str) -> List[str]:
    if not service_name in registry:
        return []
    for address, last_seen in list(registry[service_name].items()):
        if time.time() - last_seen > config.clear_timeout:
                del registry[service_name][address]
    if registry[service_name] == {}:
        del registry[service_name]
    return [address for address, last_seen in registry[service_name].items() if time.time() - last_seen <= config.down_timeout]
        


if __name__ == "__main__":
    config = DiscoveryServerConfig.load("config/discovery_server_config.json")
    uvicorn.run("discovery_server:app", host=config.host, port=config.port, reload=True)
