from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/uploadfile/")
async def uploadfile(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        return JSONResponse(content={"message": "Only text files"}, status_code=400)

    content = await file.read()

    print(content.decode("utf-8"))

    return {"filename": file.filename, "message": "file uploaded"}
