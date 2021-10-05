from discord.ext import commands


class Clean_Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clean(self, ctx, *, limit):
        try:
            await ctx.channel.purge(limit=int(limit) + 1)
        except Exception:
            pass

    @commands.command()
    async def kick(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                user = await ctx.guild.query_members(user_ids=[user.id])
            user = user[0]
            await user.kick(reason="Kicked by roBOT!")


def setup(client):
    client.add_cog(Clean_Kick(client))
