from pymongo import MongoClient
import os

CONNECTION_STRING = os.getenv("MONGO_STRING", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "dev")

connection = MongoClient(CONNECTION_STRING)
db = connection.get_database(DATABASE_NAME)

PLAYERS = db.get_collection("Players")
PLAYER_EVENTS = db.get_collection("player_events")
PLAYER_SESSIONS = db.get_collection("player_sessions")
SERVER_STATUS = db.get_collection("server_status")