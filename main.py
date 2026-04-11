from typing import Callable
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import Response
from starlette.datastructures import State
from core.rate_limit import limiter
from routers.auth import router as auth_router
import os
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Awaitable

@asynccontextmanager
async def lifespan(app: FastAPI):  
    if not os.getenv("TESTING"):
        import alembic.config
        import alembic.command
        alembic_conf = alembic.config.Config("alembic.ini")
        alembic.command.upgrade(alembic_conf, "head")
        print("✅ Database is connected") 
    yield
    print("🛑 Shutdown")
    
app = FastAPI(title="Authentication", version="0.2", lifespan=lifespan)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*']
)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request[State], call_next: Callable[[Request[State]], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
    
app.add_middleware(SecurityHeadersMiddleware)
app.include_router(auth_router, prefix="/auth")