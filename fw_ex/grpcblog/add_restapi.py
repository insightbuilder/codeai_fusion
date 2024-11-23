from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"root": "Welcome To AddMe"}


@app.get("/add/{a}/{b}")
async def addme(a: int, b: int):
    added = a + b
    return {"added": added}
