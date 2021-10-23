import discord
from stackapi import StackAPI
from discord.ext import commands
import aiohttp
import json
from command.database.loader import loader


class StackOverflow(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stack", "stackoverflow"])
    async def stack_search(self, ctx, *, args):
        try:
            async with aiohttp.ClientSession() as session:
                url = await session.get(
                    f"https://api.stackexchange.com//2.3/search/advanced?page=1&pagesize=1&order=desc&sort=activity&q={args} typeerror&site=stackoverflow".replace(
                        " ", "+"
                    )
                )
                data = await url.json()
                await ctx.send(data["items"][0]["link"])
                await ctx.message.add_reaction("\U0001f44d")
                db = loader.db_loaded()
                await db.score_up(ctx, loader.client_loaded())
        except:
            await ctx.message.add_reaction("\U0001F44E")


def setup(client):
    client.add_cog(StackOverflow(client))
