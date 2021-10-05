from discord.ext import commands


class Clean_Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, *, limit):
        await ctx.channel.purge(limit=int(limit) + 1)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                user = await ctx.guild.query_members(user_ids=[user.id])
            user = user[0]
            await user.kick(reason="Kicked by roBOT!")

    @kick.error
    @clean.error
    async def kick_clean_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.reply("You don't have permission to use this command")
            await ctx.message.add_reaction("👎")


def setup(client):
    client.add_cog(Clean_Kick(client))
