from fastapi import FastAPI

from app.api.user import router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)


# Register routes
app.include_router(router, prefix="/api")