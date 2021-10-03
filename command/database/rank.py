from command.database.loader import loader
from discord.ext import commands


class Rank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rank(self, ctx):
        db = loader.db_loaded()
        await db.rank_query(ctx.message)
        await ctx.message.add_reaction("\U0001f44d")


def setup(client):
    client.add_cog(Rank(client))