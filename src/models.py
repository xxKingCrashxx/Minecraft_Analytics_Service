import datetime
import bson
from pydantic import BaseModel

class ResponseMessage(BaseModel):
    status: int
    results: dict


class MongoModel(BaseModel):
    class Config:
        json_encoders = {
            bson.ObjectId: lambda oid: f"ObjectId('{str(oid)}')"
        }


class Player(BaseModel):
    _id: str
    player_name: str
    total_playtime: float
    first_joined: datetime.datetime
    last_seen: datetime.datetime


class PlayerInfo(BaseModel):
    player_id: str
    player_name: str


class PlayerEvent(MongoModel):
    _id: bson.ObjectId
    event_type: str
    timestamp: datetime.datetime
    event_info: PlayerInfo


class PlayerSession(MongoModel):
    _id: bson.ObjectId
    join_timestamp: datetime.datetime
    left_timestamp: datetime.datetime
    play_time: int
    session_info: PlayerInfo
  

class ServerStatus(MongoModel):
    _id: bson.ObjectId
    player_count: int
    player_list: list[PlayerInfo]
    timestamp: datetime.datetime
