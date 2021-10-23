import discord
import json
import aiohttp
from discord.ext import commands
from command.database.loader import loader


class MAL(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx, *, args):
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.jikan.moe/v3/search/anime?q={}&page=1".format(args)
                response = await session.get(url)
                data = await response.json()
                await ctx.send(data["results"][0]["url"])
                await ctx.message.add_reaction("\U0001f44d")
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())
        except:
            await ctx.message.add_reaction("\U0001f44E")

    @commands.command()
    async def manga(self, ctx, *, args):
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.jikan.moe/v3/search/manga?q={}&page=1".format(args)
                response = await session.get(url)
                data = await response.json()
                await ctx.send(data["results"][0]["url"])
                await ctx.message.add_reaction("\U0001f44d")
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())
        except:
            await ctx.message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(MAL(client))
