from fastapi import FastAPI
import uvicorn
import argparse
from routes.FirstRouter import FirstRouter
from routes.SecondRouter import SecondRouter
from fastapi import APIRouter

from py_micro_services.core import PyMicroservice

app = FastAPI()
service = PyMicroservice(config_file="config/service_config.json")

# include your routes here
FirstRouter.use_router(APIRouter(prefix="/first"))
app.include_router(FirstRouter(service).get_router(), tags=["Route 1"])

SecondRouter.use_router(APIRouter(prefix="/second"))
app.include_router(SecondRouter(service).get_router(), tags=["Second"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Hostname or IP address to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port number to bind to (default: 5000)')
    
    args = parser.parse_args()

    try:
        service.start(args.host, args.port)
        uvicorn.run("service_example:app", host=args.host, port=args.port, reload=True)
    finally:
        service.stop()

