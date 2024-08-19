from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
from os import getenv

async def validation_exception_handler(request: Request, exc: RequestValidationError):

    errors = exc.errors()
    print(errors)
    formatted_errors = []

    for error in errors:
        print('here')
        error_location = error['loc'][-1].capitalize()
        trimmed_default_error_message = ' '.join(error['msg'].split(' ')[1:])
        user_readable_error_message = f"{error_location} {trimmed_default_error_message}"
        print(user_readable_error_message)
        
        formatted_errors.append({
            "loc": error['loc'],
            "msg": user_readable_error_message,
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": formatted_errors, "body": exc.body}),
    )


async def attribute_error_handler(request: Request, exc: AttributeError):
    if getenv("ENV") == "development":
        print(f"An attribute error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A server error occured"}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    if getenv("ENV") == "development":
        print(f"HTTP exception occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):

    if isinstance(exc.orig, OperationalError):
        if getenv("ENV") == "development":
            print(f"Database error occurred: {str(exc)}")
        return JSONResponse(
            status_code=404,
            content={"detail": "Resource not found!"},
        )

    if isinstance(exc, IntegrityError):
        error_detail = "Resource already exists, unique constraint error"
        if exc.orig and hasattr(exc.orig, 'pgerror') and exc.orig.pgerror:
            error_detail += f" - Detail: {exc.orig.pgerror}"
        if getenv("ENV") == "development":
            print(f"Database error occurred: {str(exc)} - {error_detail}")
        return JSONResponse(
            status_code=409,
            content={"detail": error_detail}
        )

    if getenv("ENV") == "development":
        print(f"Database error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred"},
    )
