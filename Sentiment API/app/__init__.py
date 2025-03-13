from fastapi import FastAPI
from app.routes import router
from contextlib import asynccontextmanager
import os
import certifi
from pymongo import MongoClient
from app.config import Config

async def connectToDatabase():
    mongo_uri = os.getenv("MONGO_URI", Config.MONGO_URI)
    database_name = os.getenv("DATABASE_NAME", Config.DATABASE_NAME)
    collection_name = os.getenv("COLLECTION_NAME", Config.COLLECTION_NAME)
    
    try:
        client_mongo = MongoClient(mongo_uri)
        db = client_mongo[str(os.getenv("DATABASE_NAME"))]
        collection = db[str(os.getenv("COLLECTION_NAME"))]

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

    return collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup has begun!!")
    dbHost = await connectToDatabase()
    app.news = dbHost
    
    yield
    
    print("shutdown has begun!!")


app = FastAPI(
    title="Disaster Disruption Peripherals",
    description="This API was built with FastAPI.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router) 



