# imports
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
import models
from database import engine
from routers import todos, auth, admin, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {"status": "ok"}

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(todos.router)
