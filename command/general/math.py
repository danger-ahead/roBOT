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
    async def math(self, ctx):
        hold = ctx.message.content.find(" ")
        header = {"content-type": "application/json"}
        querystring = urllib.parse.quote_plus(
            ctx.message.content[(hold + 1) : len(ctx.message.content)]
        )

        # result = requests.get(
        #     "http://api.mathjs.org/v4/?expr=" + querystring, headers=header
        # )
        async with aiohttp.ClientSession() as session:
            response = await session.get("http://api.mathjs.org/v4/?expr=" + querystring, headers=header)
            result = response.text()
        if result.status_code == 200:
            await ctx.message.add_reaction("\U0001f44d")
            await ctx.reply("Result: " + result.text)
        else:
            await ctx.message.add_reaction("\U0001F44E")

    


def setup(client):
    client.add_cog(Math(client))