from discord.ext import commands
from command.database.loader import db_loaded


class Deconfigure(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def deconfigure(self, ctx):
        db = db_loaded()
        await db.server_deconfig(ctx.guild.id, ctx)


def setup(client):
    client.add_cog(Deconfigure(client))
