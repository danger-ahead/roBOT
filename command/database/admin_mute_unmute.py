from discord.ext import commands


class Mute_Unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
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
    async def unmute(self, ctx):
        if ctx.message.mentions.__len__() > 0:
            for user in ctx.message.mentions:
                user = await ctx.guild.query_members(user_ids=[user.id])
            user = user[0]

            try:
                await user.edit(mute=False)
            except Exception:
                pass


def setup(client):
    client.add_cog(Mute_Unmute(client))
