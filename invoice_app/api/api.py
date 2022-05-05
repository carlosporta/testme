import logging
from fastapi import FastAPI

from ..infra.db import create_db
from .routes import router


def create_app():
    app = FastAPI()

    @app.on_event('startup')
    def startup_event():
        create_db()

    app.include_router(router, prefix='/api/invoice', tags=['invoice'])
    return app
