import random

async def roll_a_dice(message):
    no = random.randint(1,6)

    if no == 1:
        await message.channel.send("|       |\n|  0  |\n|       |")
    elif no == 2:
        await message.channel.send("| 0   |\n|       |\n|   0 |")
    elif no == 3:
        await message.channel.send("|          |\n|0 0 0|\n|          |")
    elif no == 4:
        await message.channel.send("|0   0|\n|        |\n|0   0|")
    elif no == 5:
        await message.channel.send("|0   0|\n|   0   |\n|0   0|")
    else:
        await message.channel.send("|0 0 0|\n|          |\n|0 0 0|")

async def toss_coin(message):
    no = random.randint(1, 2)

    if no == 1:
        await message.channel.send('Head')
    else:
        await message.channel.send('Tail')
