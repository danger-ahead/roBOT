from discord.ext import commands
from command.database.loader import db_loaded


class Configure(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def configure(self, ctx):
        db = db_loaded()
        await db.server_config(ctx.guild.id, ctx)


def setup(client):
    client.add_cog(Configure(client))
