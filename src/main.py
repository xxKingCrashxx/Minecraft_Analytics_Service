from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from src.routes.players import player_router
from src.routes.server import server_router

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI()


app.include_router(player_router)
app.include_router(server_router)

@app.get("/")
async def root():
    return {"message": "hello world"}
