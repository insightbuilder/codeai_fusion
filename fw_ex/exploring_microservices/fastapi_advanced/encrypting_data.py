from fastapi import FastAPI
from cryptography.fernet import Fernet


app = FastAPI()

key = Fernet.generate_key()
cipher_suite = Fernet(key)


@app.post("/encrypt/")
async def encrypt_data(data: str):
    encrypt_data = cipher_suite.encrypt(data.encode())
    return {"encrypted_data": encrypt_data}
