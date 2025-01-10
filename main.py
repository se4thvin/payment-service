# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.auth_router import router as auth_router
from routers.payment_methods import router as payment_methods_router
from routers.subscriptions import router as subscriptions_router
from routers.transactions import router as transactions_router
from scheduler import scheduler, start_scheduler
from database import engine, Base

app = FastAPI(title="Payment Service")

# CORS settings
app.add_middleware(
    CORSMiddleware,
allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "http://coursebite.ai",
        "https://www.coursebite.ai",
        "https://coursebite.ai",
        "http://www.coursebite.ai",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(payment_methods_router)
app.include_router(subscriptions_router)
app.include_router(transactions_router)

@app.on_event("startup")
async def on_startup():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Start the scheduler
    scheduler.start()
    await start_scheduler()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()