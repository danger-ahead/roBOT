import discord
from command.database.loader import database
from command.database.loader import db_loaded, client_loaded
from discord.ext import commands


class Confess(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def confess(self, ctx, *, hold):
        await ctx.message.delete()
        db = db_loaded()
        client = client_loaded()
        print(hold)
        await db.confess(
            client,
            discord,
            hold,
            ctx.message,
        )


def setup(client):
    client.add_cog(Confess(client))
