from discord.ext import commands
from command.database.loader import db_loaded


class ConfigConfess_DeconfigConfess(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def configconfess(self, ctx):

        db = db_loaded()
        await db.confess_config(ctx.guild.id, ctx)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def deconfigconfess(self, ctx):

        db = db_loaded()
        await db.confess_deconfig(ctx.guild.id, ctx)

    @configconfess.error
    @deconfigconfess.error
    async def configconfess_deconfigconfess_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You don't have permission to use this command")
            await ctx.message.add_reaction("👎")


def setup(client):
    client.add_cog(ConfigConfess_DeconfigConfess(client))
