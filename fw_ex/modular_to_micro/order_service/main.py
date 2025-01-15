from fastapi import FastAPI
from redis import Redis
from routers.order_router import router as order_router
from core.database import Base, engine
from contextlib import asynccontextmanager

# Initialize Redis client
redis_client = Redis(
    host='redis',
    port=6379,
    decode_responses=True,
    retry_on_timeout=True
)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        redis_client.ping()
    except Exception as e:
        print(f"Could not connect to Redis: {e}")
        raise e
    yield
    # Shutdown
    pass

app = FastAPI(title="Order Service API", lifespan=lifespan)

# Include order router
app.include_router(order_router, prefix="/orders", tags=["Orders"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True) 