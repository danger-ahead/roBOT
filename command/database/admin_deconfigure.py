from discord.ext import commands
from command.database.loader import db_loaded


class Deconfigure(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def deconfigure(self, ctx):
        try:
            db = db_loaded()
            await db.server_deconfig(ctx.guild.id, ctx)
            await ctx.message.add_reaction("\U0001f44d")
        except:
            await ctx.message.add_reaction("\U0001f44E")


def setup(client):
    client.add_cog(Deconfigure(client))
