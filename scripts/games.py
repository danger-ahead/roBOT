import random

async def roll_a_dice(message):
    number = random.randint(1, 6)

    if number == 1:
        await message.channel.send("|       |\n|  0  |\n|       |")
    elif number == 2:
        await message.channel.send("| 0   |\n|       |\n|   0 |")
    elif number == 3:
        await message.channel.send("|          |\n|0 0 0|\n|          |")
    elif number == 4:
        await message.channel.send("|0   0|\n|        |\n|0   0|")
    elif number == 5:
        await message.channel.send("|0   0|\n|   0   |\n|0   0|")
    else:
        await message.channel.send("|0 0 0|\n|          |\n|0 0 0|")

async def toss_coin(message):
    number = random.randint(1, 2)

    if number == 1:
        await message.channel.send('Head')
    else:
        await message.channel.send('Tail')
