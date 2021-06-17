import random
import discord


async def roll_a_dice(discord, message):
    number = random.randint(1, 6)

    if number == 1:
        embed = discord.Embed(
            title="Dice!!",
            description="|--------|\n|---0---|\n|--------|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
    elif number == 2:
        embed = discord.Embed(
            title="Dice!!",
            description="|-0---|\n|------|\n|---0-|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
    elif number == 3:
        embed = discord.Embed(
            title="Dice!!",
            description="|---------|\n|0--0--0|\n|---------|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
    elif number == 4:
        embed = discord.Embed(
            title="Dice!!",
            description="|0---0|\n|-------|\n|0---0|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
    elif number == 5:
        embed = discord.Embed(
            title="Dice!!",
            description="|0----0|\n|---0---|\n|0----0|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Dice!!",
            description="|0 0 0|\n|------|\n|0 0 0|",
            color=discord.Color.blue(),
        )
        await message.channel.send(embed=embed)

    await message.add_reaction("\U0001f44d")


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
