import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from wiring import wire_dependencies
from database import AsyncSessionLocal, close_db, engine
from database import Base, init_models
from shared.core.exception_handlers import register_exception_handlers
from shared.core.middlewares import register_middleware_handlers
from shared.infrastructure.demo_seed import seed_demo_data
from user.presentation.router import router as user_router
from auth.presentation.router import router as auth_router
from board.presentation.router import router as board_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models()
    # create_all creates missing tables; it is not a migration tool.
    if os.getenv("CREATE_TABLES", "false").lower() == "true":
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    if os.getenv("DEMO_SEED", "false").lower() == "true":
        async with AsyncSessionLocal() as session:
            await seed_demo_data(session)
    try:
        yield
    finally:
        await close_db()

app = FastAPI(title="Board API", version="1.0.0",
              description="교안 기반 4계층 게시판 API", lifespan=lifespan)
register_exception_handlers(app)
register_middleware_handlers(app)
wire_dependencies(app)
for router in (user_router, auth_router, board_router):
    app.include_router(router)

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
