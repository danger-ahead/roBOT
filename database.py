import pymongo as pm
# from pymongo import MongoClient
from decouple import config

class database:
    def __init__(self):
        cluster = pm.MongoClient("mongodb+srv://danger-ahead:"+config('MONGO')+"@cluster0.z0zou.mongodb.net/test")
        db = cluster["roBOT"]
        collection = db["user_score"]

