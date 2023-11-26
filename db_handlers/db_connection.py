from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://buddy:60KhZZHdv5EaPyqPMEf7@cluster0.gloaamf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

def get_db():
    return client['just6botbase']
