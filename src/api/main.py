from fastapi import FastAPI
from database import SessionLocal, Base, engine
from logger import logger

app = FastAPI()

@app.on_event("startup")
def startup():
    logger.info("Connecting to the database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database connected and tables created (if not exist)")

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down, database engine disposed.")
    engine.dispose()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()