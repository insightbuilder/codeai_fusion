import onnxruntime as ort
from fastapi import FastAPI

app = FastAPI()

session = ort.onnxruntime("model.onnx")


@app.post("/predict/")
async def predict(data: dict):
    inputs = {session.get_inputs()[0].name: [data["input"]]}
    result = session.run(None, inputs)
    return {"prediction": result}
