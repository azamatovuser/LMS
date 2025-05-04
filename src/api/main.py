from fastapi import FastAPI
from api.database import Base, engine
from api.logger import logger
from api.routers.account import router as account_router

app = FastAPI()

app.include_router(account_router, prefix="/api/account", tags=["Account"])

@app.on_event("startup")
def startup():
    logger.info("Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database connected and tables created (if not exist)")

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down, database engine disposed.")
    engine.dispose()
