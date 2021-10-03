import discord
from command.database.loader import database
from command.database.loader import db_loaded, client_loaded
from discord.ext import commands


class Confess(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.command()
    async def confess(self, ctx):
        await ctx.message.delete()
        db = db_loaded()
        client = client_loaded()
        hold = ctx.message.content.find(" ")  # searches for the first space after the command
        await db.confess(
            client,
            discord,
            ctx.message.content[(hold + 1) : len(ctx.message.content)],
            ctx.message,
        )



def setup(client):
    client.add_cog(Confess(client))