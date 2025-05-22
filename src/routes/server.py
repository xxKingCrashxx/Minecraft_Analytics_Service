from fastapi import APIRouter
from fastapi import HTTPException
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from datetime import date, datetime, time, timedelta, timezone
from src.db_constants import SERVER_STATUS, PLAYER_EVENTS
from src.models import ServerStatus, InferredPlayerInfo, ResponseMessage
server_router = APIRouter(
    prefix="/api/server",
    tags=["server"]
)

@server_router.get("/latest_status", response_model=ResponseMessage)
def get_latest_server_status():
    latest_status = SERVER_STATUS.find_one({}, sort=[{"timestamp", DESCENDING}])

    if not latest_status:
        return ResponseMessage(status=200, results={
            "latest_status": None,
        })

    return ResponseMessage(
        status=200,
        results={
            "latest_status": ServerStatus(
                _id=ObjectId(latest_status["_id"]),
                timestamp=latest_status["timestamp"],
                player_count=latest_status["player_count"],
                player_list=[
                    InferredPlayerInfo(
                        player_id=p["player_id"],
                        player_name=p["player_name"],
                        confidence_score_online=p["confidence_score_online"],
                    )
                    for p in latest_status["player_list"]
                ]
            )
        }
    )
