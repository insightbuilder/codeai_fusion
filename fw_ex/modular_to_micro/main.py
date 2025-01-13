from fastapi import FastAPI
from routers.user_router import router as user_router
from routers.order_router import router as order_router
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Modular Monolith API")

# Include routers with authentication dependency
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
