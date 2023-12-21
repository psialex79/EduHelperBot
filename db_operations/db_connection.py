"""Модуль для подключения к базе данных MongoDB."""

from pymongo import MongoClient
from pymongo.server_api import ServerApi

# URI базы данных MongoDB
URI = (
    "mongodb+srv://buddy:60KhZZHdv5EaPyqPMEf7@cluster0.gloaamf.mongodb.net/"
    "?retryWrites=true&w=majority"
)

client = MongoClient(URI, server_api=ServerApi('1'))

def get_db():
    """Возвращает экземпляр базы данных just6botbase."""
    return client['just6botbase']
