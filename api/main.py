import uvicorn
from os import getenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from database.database import engine, Base
from database.database_utils.get_db import get_db

from api.errors.error_handling import (
    validation_exception_handler, attribute_error_handler,  http_exception_handler, sqlalchemy_exception_handler)

import api.routes.auth as auth_route
import api.routes.campsites as campsites_route
import api.routes.users as users_route

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = [
    'http://localhost:8081'  # localhost address for development
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_route.router)
app.include_router(campsites_route.router)
app.include_router(users_route.router)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AttributeError, attribute_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"Server": "Healthy and happy!"}


if __name__ == "__main__":
    PORT = int(getenv('PORT', 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
