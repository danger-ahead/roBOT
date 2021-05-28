import pymongo as pm
# from pymongo import MongoClient
from decouple import config

class Database:
    def __init__(self):
        print('Running: database.py')

    async def score_up(self, id):
        score = -1
        cluster = pm.MongoClient("mongodb+srv://danger-ahead:"+config('MONGO')+"@cluster0.z0zou.mongodb.net/test")
        db = cluster["roBOT"]
        collection = db["user_score"]
        query = {"_id": id}
        user = collection.find(query)
        for result in user:
            score = result["score"]

        if score > 0:
            score = score + 1
            collection.update_one({"_id":id}, {"$set":{"score":score}})
        else:
            collection.insert_one({"_id":id, "score":1})