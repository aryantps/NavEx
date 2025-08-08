from app.middleware.request_id import RequestIDMiddleware
from fastapi import FastAPI, Request, HTTPException
from app.api.v1.tracking import router as tracking_router
from app.api.v1.vehicle_type import router as vehicle_type_router
from app.api.v1.vehicle import router as vehicle_router
from app.api.v1.location import router as location_router
from app.api.v1.driver_details import router as driver_details_router
from app.api.v1.trip import router as trip_router
from app.core.startup_events import register_startup_events


from app.core.logger import logger 
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.schemas.response import APIResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR



def create_app() -> FastAPI:
    app = FastAPI(title="Logistics Management API")
    app.add_middleware(RequestIDMiddleware)
    register_routes(app)
    register_startup_events(app)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}
    


    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(f"HTTPException: {exc.detail} (status_code={exc.status_code})")
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(success=False, code=exc.status_code, message=exc.detail).dict()
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"IntegrityError: {exc}")
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content=APIResponse(success=False, code=HTTP_400_BAD_REQUEST, message="Database integrity error.").dict()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content=APIResponse(success=False, code=HTTP_500_INTERNAL_SERVER_ERROR,
                                message="Internal server error. Please try again later.").dict()
        )

    return app


def register_routes(app: FastAPI):
    app.include_router(trip_router, prefix="/api/v1/trips", tags=["Trips"])
    app.include_router(tracking_router, prefix="/api/v1/tracking", tags=["Tracking"])
    app.include_router(vehicle_type_router, prefix="/api/v1/vehicle-types", tags=["Vehicle Types"])
    app.include_router(vehicle_router, prefix="/api/v1/vehicle", tags=["Vehicles"])
    app.include_router(location_router, prefix="/api/v1/location", tags=["Locations"])
    app.include_router(driver_details_router, prefix="/api/v1/drivers", tags=["Drivers"])
