import aiohttp
import urllib
from discord.ext import commands

class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    """
    ISSUE:
    i dk about this api,
    please test it out & fix it
    """

    @commands.command()
    async def math(self, ctx, querystring):
        hold = ctx.message.content.find(" ")
        header = {"content-type": "application/json"}
        querystring = urllib.parse.quote_plus(
            ctx.message.content[(hold + 1) : len(ctx.message.content)]
        )

        async with aiohttp.ClientSession() as session:
            response = await session.get("http://api.mathjs.org/v4/?expr=" + querystring, headers=header)
            result = await response.text()
        if response.status == 200:
            await ctx.send(f"**Result:** `{result}`")
            await ctx.message.add_reaction("\U0001f44d")
        else:
            await ctx.message.add_reaction("\U0001F44E")

    


def setup(client):
    client.add_cog(Math(client))