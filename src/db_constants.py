from pymongo import MongoClient
import os

MONGO_STRING = os.getenv("MONGO_STRING", "localhost")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "dev")

connection = MongoClient(MONGO_STRING)
db = connection.get_database(MONGO_DATABASE_NAME)

PLAYERS = db.get_collection("Players")
PLAYER_EVENTS = db.get_collection("player_events")
PLAYER_SESSIONS = db.get_collection("player_sessions")
SERVER_STATUS = db.get_collection("server_status")