from fastapi import FastAPI

from app.database import Base, engine

from app.routes.auth_routes import router as auth_router
from app.routes.notes_routes import router as notes_router
from app.routes.about_routes import router as about_router
from app.routes.share_routes import router as share_router
from app.routes.history_routes import router as history_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes API"
)

app.include_router(share_router)
app.include_router(history_router)

app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(about_router)