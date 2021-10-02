import os
import random
import discord
from discord.ext import commands

class Roll(commands.Cog):
    def __init__(self, client):
        self.client = client

    # this is roll a dice command
    @commands.command(aliases = ['roll', 'dice'])
    async def roll_a_dice(self, ctx):
        number = random.randint(1, 6)
        cwd = os.getcwd()  # stores current directory before changing
        os.chdir("images")  # changes to the images directory

        if number == 1:
            await ctx.reply(file=discord.File("dice1.jpg"))
        elif number == 2:
            await ctx.reply(file=discord.File("dice2.jpg"))
        elif number == 3:
            await ctx.reply(file=discord.File("dice3.jpg"))
        elif number == 4:
            await ctx.reply(file=discord.File("dice4.jpg"))
        elif number == 5:
            await ctx.reply(file=discord.File("dice5.jpg"))
        else:
            await ctx.reply(file=discord.File("dice6.jpg"))

        await ctx.message.add_reaction("\U0001f44d")

        os.chdir(cwd)  # changes back to the previously stored directory

def setup(client):
    client.add_cog(Roll(client))