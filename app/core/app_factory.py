from app.middleware.request_id import RequestIDMiddleware
from app.middleware.auth_user_context import JWTAuthMiddlewareRS256
from fastapi import FastAPI, HTTPException
from app.api.v1.tracking import router as tracking_router
from app.api.v1.vehicle_type import router as vehicle_type_router
from app.api.v1.vehicle import router as vehicle_router
from app.api.v1.location import router as location_router
from app.api.v1.driver_details import router as driver_details_router
from app.api.v1.trip import router as trip_router
from app.api.v1.tenant import router as tenant_router
from app.api.v1.user import router as user_router
from app.api.v1.role import router as role_router
from app.api.v1.user_role import router as user_role_router
from app.core.startup_events import lifespan

from fastapi.openapi.utils import get_openapi

from sqlalchemy.exc import (
    IntegrityError,
    ArgumentError,
    OperationalError,
    ProgrammingError,
    DataError,
)

from app.core.exception_handlers import (
    http_exception_handler,
    integrity_error_handler,
    argument_error_handler,
    operational_error_handler,
    programming_error_handler,
    data_error_handler,
    generic_exception_handler,
)

def create_app() -> FastAPI:
    app = FastAPI(
        title="NavEx",
        lifespan=lifespan
    )
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(JWTAuthMiddlewareRS256)
    register_routes(app)
    register_exception_handlers(app)

    app.openapi = custom_openapi_factory(app)

    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    return app


def register_routes(app: FastAPI):
    app.include_router(tenant_router, prefix="/api/v1/tenants", tags=["Tenants"])
    app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(role_router, prefix="/api/v1/roles", tags=["Roles"])
    app.include_router(user_role_router, prefix="/api/v1/user-roles", tags=["User Roles"])
    app.include_router(trip_router, prefix="/api/v1/trips", tags=["Trips"])
    app.include_router(tracking_router, prefix="/api/v1/tracking-records", tags=["Vehicle Tracking"])
    app.include_router(vehicle_type_router, prefix="/api/v1/vehicle-types", tags=["Vehicle Types"])
    app.include_router(vehicle_router, prefix="/api/v1/vehicle", tags=["Vehicles"])
    app.include_router(location_router, prefix="/api/v1/location", tags=["Locations"])
    app.include_router(driver_details_router, prefix="/api/v1/drivers", tags=["Drivers"])




def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(ArgumentError, argument_error_handler)
    app.add_exception_handler(OperationalError, operational_error_handler)
    app.add_exception_handler(ProgrammingError, programming_error_handler)
    app.add_exception_handler(DataError, data_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


def custom_openapi_factory(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="NavEx API",
            version="1.0.0",
            description="API for the NavEx multi-tenant fleet system",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        for path in openapi_schema["paths"].values():
            for operation in path.values():
                operation["security"] = [{"BearerAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return custom_openapi
