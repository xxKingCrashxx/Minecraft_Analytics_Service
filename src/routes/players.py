from fastapi import APIRouter
from fastapi import HTTPException
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from datetime import date, datetime, time, timedelta, timezone

from src.models import ResponseMessage, PlayerSession, PlayerInfo
from src.db_constants import PLAYER_EVENTS, PLAYER_SESSIONS, PLAYERS, MONGO_DATABASE_NAME

player_router = APIRouter(
    prefix="/api/players",
    tags=["players"]
)

@player_router.get("/", response_model=ResponseMessage)
# return a list of all players that have joined the server.
def get_all_unique_players(limit:int = 100, page: int = 1, sort="last_seen"):

    skip = limit * (page - 1)

    if limit < 1 or page < 1:
        raise HTTPException(400, "Invalid Query Parameters")
    
    player_cursor = PLAYERS.find(
        {},
        {   
            "player_name": 1,
            "last_seen": 1,
            "_id": 1
        },
        skip=skip,
        limit=limit,
        sort=[(sort, DESCENDING)] 
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

@player_router.get("/{player_username}/sessions", response_model=ResponseMessage)
def get_player_sessions(
        player_username: str,
        limit: int = 100,
        page:int = 1, 
        date_start: datetime = None, 
        date_end: datetime = None
    ):
        if limit < 1 or page < 1:
            raise HTTPException(400, "Invalid pagination parameters")
        
        skip = limit * (page - 1)

        if date_end is None:
             date_end = datetime.now(tz=timezone.utc)

        if date_start is None:
             date_start = date_end - timedelta(days=1)
             date_start.replace(tzinfo=timezone.utc)

        print(date_start.isoformat())
        print(date_end.isoformat())
        print(MONGO_DATABASE_NAME)

        query = {
                    "session_info.player_name": player_username,
                    "play_time": {"$gt": 0},
                    "join_timestamp": {
                        "$gte": date_start,
                        "$lt": date_end
                    }
                }
        
        total_count = PLAYER_SESSIONS.count_documents(query)

        session_cursor = PLAYER_SESSIONS.find(
            query,
            limit=limit,
            skip=skip,
            sort=[("join_timestamp", ASCENDING)]

        )

        session_list = list(session_cursor)
        return ResponseMessage(status=200, results={
                "page": f"{page}/{(total_count + limit - 1) // limit}",
                "limit": limit,
                "total": total_count,
                "sessions": [
                    PlayerSession(
                        _id=str(session["_id"]),
                        join_timestamp=session["join_timestamp"],
                        left_timestamp=session["left_timestamp"],
                        play_time=session["play_time"],
                        session_info=PlayerInfo(
                            player_name=session["session_info"]["player_name"], 
                            player_id=session["session_info"]["player_id"]
                        )
                    )
                    for session in session_list
                ]
            }
        )

    

