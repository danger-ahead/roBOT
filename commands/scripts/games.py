import random
import discord
import os


async def roll_a_dice(discord, message):
    number = random.randint(1, 6)
    cwd = os.getcwd()  # stores current directory before changing
    os.chdir("scripts/images")  # changes to the images directory

    if number == 1:
        await message.reply(file=discord.File("dice1.jpg"))
    elif number == 2:
        await message.reply(file=discord.File("dice2.jpg"))
    elif number == 3:
        await message.reply(file=discord.File("dice3.jpg"))
    elif number == 4:
        await message.reply(file=discord.File("dice4.jpg"))
    elif number == 5:
        await message.reply(file=discord.File("dice5.jpg"))
    else:
        await message.reply(file=discord.File("dice6.jpg"))

    await message.add_reaction("\U0001f44d")

    os.chdir(cwd)  # changes back to the previously stored directory


async def toss_coin(discord, message):
    number = random.randint(1, 2)

    if number == 1:
        embed = discord.Embed(
            title="Toss!!", description="Head", color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Toss!!", description="Tails", color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)

    await message.add_reaction("\U0001f44d")
