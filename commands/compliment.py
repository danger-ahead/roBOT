"""
Module containing the functions for _compliment command.

"""
import random


async def comp(discord, message):
    compliments = [
        "You are more fun than bubble wrap",
        "You are the most perfect you there is.",
        "You are enough.",
        "You are one of the smartest people I know.",
        "You look great today.",
        "You have the best smile.",
        "You light up the whole server.",
        "You are doing great.Keep going!",
    ]
    response = random.choice(compliments)
    await message.channel.send(response)
    await message.author.send(response)
