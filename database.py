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
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell != '':
            await message.channel.send('I\'m already configured on <#'+str(channell)+'>')
        else:
            self.collection2.insert_one({"_id":server, "channel":channel, "confess":0})
            await message.channel.send('I just got configured!')

    async def server_deconfig(self, server, channel, message):
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell == channel:
            self.collection2.delete_one( {"_id": server})
            await message.channel.send('I\'ve been deconfigured!')
        elif channell != channel:
            await message.channel.send('I\'m configured on <#'+str(channell)+'> \nI can\'t deconfigure here!')

    async def confess_config(self, server, channel, message):
        confess = 0
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            confess = result["confess"]
            channell = result["channel"]

        if confess != 0:
            await message.channel.send('I\'m already configured on <#'+str(confess)+'>')
        else:
            self.collection2.update_one({"_id" : server}, {"$set" : {"_id" : server, "channel" : channell, "confess":channel}})
            await message.channel.send('I just got the confession channel configured!')

    async def confess_deconfig(self, server, channel, message):
        confess = 0
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            confess = result["confess"]
            channell = result["channel"]

        if confess == channel:
            self.collection2.update_one({"_id" : server}, {"$set" : {"_id" : server, "channel" : channell, "confess":0}})
            await message.channel.send('My confession channel has been deconfigured!')
        elif confess != channel:
            await message.channel.send('My confession channel is configured on <#'+str(confess)+'> \nI can\'t deconfigure here!')

    async def leave_server(self, server, channel, message):
        channell = ''
        query = {"_id": server}
        user = self.collection2.find(query)
        for result in user:
            channell = result["channel"]

        if channell == channel:
            await message.channel.send('Don\'t want me? Fine!')
            await message.guild.leave()
        elif channell == '':
            await message.channel.send('Configure me first!')
        else:
            await message.channel.send('I\'ll only leave if instructed from <#'+str(channell)+'>')

    async def confess(self, client, discord, confession, message):
        channell = 0
        user = self.collection2.find({"_id":message.guild.id})
        for result in user:
            channell = result["confess"]

        if channell != 0:
            embed=discord.Embed(title='Someone just confessed:', description=confession, color=discord.Color.blue())
            await client.get_channel(channell).send(embed=embed)
        else:
            await message.channel.send('My confession channel hasn\'t been configured!')