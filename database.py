import pymongo as pm
from decouple import config

class Database:
    def __init__(self):
        self.cluster = pm.MongoClient("mongodb+srv://danger-ahead:"+config('MONGO')+"@cluster0.z0zou.mongodb.net/test")
        self.db = self.cluster["roBOT"]
        self.collection = self.db["user_score"]
        self.collection2 = self.db["servers"]
        print('Running: Database module [database.py]\n')

    async def score_up(self, id, message, channel, client):
        score = -1
        query = {"_id": id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]

        if score > 0:
            score = score + 1
            self.collection.update_one({"_id":id}, {"$set":{"score":score}})

            if(score%15 == 0):
                user = self.collection2.find({"_id":message.guild.id})
                for result in user:
                    channell = result["channel"]

                chanell = client.get_channel(channell)
                await chanell.send(message.author.mention+', you\'re my level '+str(int(score/15))+ ' friend now!')
        else:
            self.collection.insert_one({"_id":id, "score":1})

    async def rank_query(self, id, message, channel):
        query = {"_id": id}
        user = self.collection.find(query)
        for result in user:
            score = result["score"]
        await message.channel.send(message.author.mention+', you\'re my level '+str(int(score/15))+ ' friend!')

    async def server_config(self, server, channel, message):
        if (self.collection2.count_documents({"_id":server}) == 0):
            self.collection2.insert_one({"_id":server, "channel":channel})
            await message.channel.send('roBOT configured!')
        else:
            self.collection2.update_one({"_id":server}, {"$set":{"channel":channel}})
            await message.channel.send('roBOT configuration updated!')        

    async def leave_server(self, server, channel, message):
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell == channel:
            await message.channel.send('Don\'t want me? Fine!')
            await message.guild.leave()
        else:
            await message.channel.send('I\'ll only leave if instructed from <#'+str(channell)+'>')