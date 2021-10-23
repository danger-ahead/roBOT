import os
import dotenv
import aiohttp
from discord.ext import commands
from command.database.loader import loader

dotenv.load_dotenv()


class Song(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def song(self, ctx, *, hold="song"):
        querystring = {"q": hold}

        headers = {
            "x-rapidapi-key": str(os.getenv("RAPID_API")),
            "x-rapidapi-host": "genius.p.rapidapi.com",
        }

        async with aiohttp.ClientSession() as session:

            response = await session.get(
                "https://genius.p.rapidapi.com/search",
                headers=headers,
                params=querystring,
            )
            try:
                data = await response.json()
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
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())
            except:
                await ctx.message.add_reaction("\U0001F44E")


def setup(client):
    client.add_cog(Song(client))
