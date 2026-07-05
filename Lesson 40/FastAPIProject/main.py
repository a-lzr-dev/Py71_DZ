from fastapi import FastAPI

from src.routers.admin import router as admin_router
from src.routers.auth import router as auth_router
from src.routers.events import router as events_router
from src.routers.users import router as users_router

app = FastAPI(title="Events API", version="1.0")

prefix = "/api/v1"
app.include_router(admin_router, prefix="/admin")
app.include_router(auth_router, prefix=prefix)
app.include_router(events_router, prefix=prefix)
app.include_router(users_router, prefix=prefix)