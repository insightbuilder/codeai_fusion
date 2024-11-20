import os
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": f'{os.environ.get("HOSTNAME", "DefaultENV")}'}

# Liveness endpoint
@app.get("/health/live")
def liveness():
    # Logic to check if the app is running (always returns OK for now)
    return {"status": "ok"}

# Readiness endpoint
@app.get("/health/ready")
def readiness():
    # Logic to check if dependencies are ready (e.g., database, cache)
    # Add checks for critical services here if needed.
    return {"status": "ok"}

@app.on_event("shutdown")
async def shutdown():
    print("Shutting down gracefully...")
