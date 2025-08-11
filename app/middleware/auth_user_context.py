from typing import Callable

import jwt
from jwt import PyJWTError
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from uvicorn.main import logger

from app.core.config import get_settings

settings = get_settings()

EXEMPT_PATHS = {"/docs", "/openapi.json"}
EXEMPT_PREFIXES = ["/open"]


class JWTAuthMiddlewareRS256(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path

        if any(path.startswith(prefix) for prefix in EXEMPT_PREFIXES) or path in EXEMPT_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Missing Authorization header"},
            )

        try:
            scheme, token = auth_header.split(" ")
        except ValueError:
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Invalid Authorization header format"},
            )

        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Authorization scheme must be Bearer"},
            )

        try:
            payload = jwt.decode(
                token,
                settings.AUTH_PUBLIC_KEY,
                algorithms=[settings.AUTH_ALGORITHM],
                audience=settings.AUTH_AUDIENCE,
                issuer=settings.AUTH_ISSUER,
            )
            user_id = payload.get("sub")
            if user_id:
                request.state.user_id = user_id
                request.state.user = payload
            else:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Unauthorized", "message": "Invalid token payload"},
                )
        except PyJWTError as e:
            logger.error(f"JWTAuthMiddlewareRS256: JWT decode error - {e} path={path} client={request.client.host}")
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Invalid or expired token"},
            )

        return await call_next(request)