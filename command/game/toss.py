import random
import discord
from discord.ext import commands

class Toss(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['toss','coin'])
    async def toss_coin(self, ctx):
        number = random.randint(1, 2)

        if number == 1:
            embed = discord.Embed(
                title="Toss!!", description="Head", color=discord.Color.blue()
            )
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Toss!!", description="Tails", color=discord.Color.blue()
            )
            await ctx.reply(embed=embed)

        await ctx.message.add_reaction("\U0001f44d")

def setup(client):
    client.add_cog(Toss(client))