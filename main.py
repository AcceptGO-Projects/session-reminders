from fastapi import FastAPI
from app.api.routes import router as api_router
from app.config.data_source import engine
from app.services.scheduler_service import scheduler
from app.models import user, reminder, user_reminder, course, user_course
from fastapi.middleware.cors import CORSMiddleware
import contextlib
from fastapi.responses import HTMLResponse

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(reminder.Base.metadata.create_all)
        await conn.run_sync(user_reminder.Base.metadata.create_all)
        await conn.run_sync(course.Base.metadata.create_all)
        await conn.run_sync(user_course.Base.metadata.create_all)
    if not scheduler.running:
        scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

VERSION = "/api/v1"

app.include_router(api_router, prefix=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <h1 style="text-align:center;">Server is Running!</h1>
    """
