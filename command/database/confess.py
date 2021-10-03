import discord
from command.database.loader import database
from command.database.loader import loader
from discord.ext import commands


class Confess(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    async def confess(self, ctx):
        await ctx.message.delete()
        db = loader.db_loaded()
        client = loader.client_loaded()
        hold = ctx.message.content.find(" ")  # searches for the first space after the command
        await db.confess(
            client,
            discord,
            ctx.message.content[(hold + 1) : len(ctx.message.content)],
            ctx.message,
        )



def setup(client):
    client.add_cog(Confess(client))