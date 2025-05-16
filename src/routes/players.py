from fastapi import APIRouter
from src.models import ResponseMessage
from src.db_constants import PLAYER_EVENTS, PLAYER_SESSIONS, PLAYERS

player_router = APIRouter(
    prefix="/api/players",
    tags=["players"]
)

@player_router.get("/", response_model=ResponseMessage)
# return a list of all players that have joined the server.
def get_all_unique_players():
    player_cursor = PLAYERS.find(
        {},
        {   
            "player_name": 1,
            "_id": 1
        } 
    )
    player_list = list(player_cursor)
    return {
        "status": 200,
        "results": {
            "count": len(player_list),
            "players": player_list,
        }
    }

@player_router.get("/{player_username}", response_model=ResponseMessage)
def get_player(player_username: str):
    player = PLAYERS.find_one({"player_name": player_username})

    if player is None:
        return ResponseMessage(status=200, results={})
    else:
        return ResponseMessage(status=200, results={
            "player": player
        })

