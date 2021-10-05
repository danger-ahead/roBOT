from discord.ext import commands


class Mute_Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                user = await ctx.guild.query_members(user_ids=[user.id])
            user = user[0]

            try:
                await user.edit(mute=True)
            except Exception:
                pass

    @commands.command()
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                user = await ctx.guild.query_members(user_ids=[user.id])
            user = user[0]

            try:
                await user.edit(mute=False)
            except Exception:
                pass

    @mute.error
    @unmute.error
    async def mute_unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You don't have permission to use this command")
            await ctx.message.add_reaction("👎")


def setup(client):
    client.add_cog(Mute_Unmute(client))
