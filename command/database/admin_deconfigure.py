from discord.ext import commands
from command.database.loader import db_loaded


class Deconfigure(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def deconfigure(self, ctx):

        db = db_loaded()
        await db.server_deconfig(ctx.guild.id, ctx)

    @deconfigure.error
    async def configure_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You don't have permission to use this command")
            await ctx.message.add_reaction("👎")


def setup(client):
    client.add_cog(Deconfigure(client))
