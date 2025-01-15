from fastapi import FastAPI
from redis import Redis
from user_router import router as user_router
from core.database import Base, engine
from contextlib import asynccontextmanager
import json
from fastapi.background import BackgroundTasks

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

app = FastAPI(title="User Service API", lifespan=lifespan)

# Include user router
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Add this function to handle Redis subscriptions
async def handle_user_verification_requests():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('verify_user')
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = json.loads(message['data'])
            user_id = data.get('user_id')
            # Verify user and publish response
            user = verify_user(user_id)  # Your verification logic
            response = {'user_id': user_id, 'is_valid': bool(user)}
            redis_client.publish('user_verification_response', json.dumps(response))

async def verify_user(user_id: str):
    # First check cache
    cached_user = redis_client.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # If not in cache, check database
    db = SessionLocal()
    try:
        user = get_user_by_username(db, user_id)
        if user:
            # Cache the user data for 1 hour
            user_data = {"id": user.id, "username": user.username}
            redis_client.setex(f"user:{user_id}", 3600, json.dumps(user_data))
            return user_data
        return None
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True) 