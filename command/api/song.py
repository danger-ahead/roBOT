import os
import json
import dotenv
import requests
from discord.ext import commands

dotenv.load_dotenv()

class Song(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def song(self, ctx):
        hold = ctx.message.content.find(" ")
        querystring = {"q": ctx.message.content[(hold + 1) : len(ctx.message.content)]}

        headers = {
            "x-rapidapi-key": str(os.getenv("RAPID_API")),
            "x-rapidapi-host": "genius.p.rapidapi.com",
        }

        response = requests.request(
            "GET",
            "https://genius.p.rapidapi.com/search",
            headers=headers,
            params=querystring,
        )
        try:
            data = json.loads(response.text)
            response1 = data["response"]
            hits = response1["hits"]

            for i in range(1):
                x = hits[i]
                y = x["result"]
                await ctx.send(
                    "'"
                    + y["full_title"]
                    + "'"
                    + "\nDetails of the song can be found at: "
                    + y["url"]
                )
            await ctx.message.add_reaction("\U0001f44d")
        except:
            await ctx.message.add_reaction("\U0001F44E")

def setup(client):
    client.add_cog(Song(client))