import pymongo as pm
from decouple import config

class Database:
    def __init__(self):
        self.cluster = pm.MongoClient("mongodb+srv://danger-ahead:"+config('MONGO')+"@cluster0.z0zou.mongodb.net/test")
        self.db = self.cluster["roBOT"]
        self.collection = self.db["user_score"]
        print('Running: Database module [database.py]\n')

    async def score_up(self, id, message, channel):
        score = -1
        query = {"_id": id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]

        if score > 0:
            score = score + 1
            self.collection.update_one({"_id":id}, {"$set":{"score":score}})
            if(score%20 == 0):
                await message.channel.send(message.author.mention+', you\'re now my level '+str(int(score/20))+ ' friend')
        else:
            self.collection.insert_one({"_id":id, "score":1})

    async def rank_query(self, id, message, channel):
        query = {"_id": id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]
        await message.channel.send(message.author.mention+', you\'re my level '+str(int(score/20))+ ' friend')