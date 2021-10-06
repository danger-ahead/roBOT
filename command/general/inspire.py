import aiohttp
from discord.ext import commands
from command.database.loader import loader


class Inspire(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_quote(self):
        async with aiohttp.ClientSession() as session:
            url = "https://zenquotes.io/api/random"
            response = await session.get(url)
            json_data = await response.json(content_type="text/plain")

            quote = json_data[0]["q"] + " -" + json_data[0]["a"]
            return quote

    @commands.command()
    async def inspire(self, ctx):
        try:
            quote = await Inspire.get_quote(self)
            await ctx.send(quote)
            await ctx.message.add_reaction("\U0001f44d")
            db = loader.db_loaded()
            await db.score_up(ctx, loader.client_loaded())
        except Exception as e:
            await ctx.message.add_reaction("\U0001F44E")
            await ctx.send("Quota exhausted :(\nTry again later!")


def setup(client):
    client.add_cog(Inspire(client))
