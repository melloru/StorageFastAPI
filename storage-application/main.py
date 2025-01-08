from fastapi import FastAPI
import uvicorn
from api import router as storage_router
from core.config import Settings, settings

app = FastAPI()

app.include_router(storage_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
