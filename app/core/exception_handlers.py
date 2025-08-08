from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import (
    IntegrityError,
    ArgumentError,
    OperationalError,
    ProgrammingError,
    DataError,
)
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from app.schemas.response import APIResponse
from app.core.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail} (status_code={exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(success=False, code=exc.status_code, message=exc.detail).dict(exclude_none=True)
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"IntegrityError: {exc}")
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=APIResponse(
            success=False,
            code=HTTP_400_BAD_REQUEST,
            message="Database integrity error.",
        ).dict(exclude_none=True),
    )


async def argument_error_handler(request: Request, exc: ArgumentError):
    logger.error(f"SQL ArgumentError: {exc}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse(
            success=False,
            code=HTTP_422_UNPROCESSABLE_ENTITY,
            message="Invalid database argument or schema.",
        ).dict(exclude_none=True),
    )


async def operational_error_handler(request: Request, exc: OperationalError):
    logger.error(f"OperationalError: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            success=False,
            code=HTTP_500_INTERNAL_SERVER_ERROR,
            message="Database operation failed. Try again later.",
        ).dict(exclude_none=True),
    )


async def programming_error_handler(request: Request, exc: ProgrammingError):
    logger.error(f"ProgrammingError: {exc}")
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content=APIResponse(
            success=False,
            code=HTTP_400_BAD_REQUEST,
            message="SQL query error. Please check your schema.",
        ).dict(exclude_none=True),
    )


async def data_error_handler(request: Request, exc: DataError):
    logger.error(f"DataError: {exc}")
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse(
            success=False,
            code=HTTP_422_UNPROCESSABLE_ENTITY,
            message="Invalid data for one or more fields.",
        ).dict(exclude_none=True),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            success=False,
            code=HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error. Please try again later.",
        ).dict(exclude_none=True),
    )
