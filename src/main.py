from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}
