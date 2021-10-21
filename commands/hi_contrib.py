"""
Module containing the functions for _hi and _contribute commands.
"""


async def hi(discord, message):
    embed = discord.Embed(
        title="🙏🏻 Hello my friend!!, myself roBOT!",
        description="An amatuer bot by amatuer Developers!! 😂 \
        \n Want to play with me?\
        \nVisit: https://github.com/danger-ahead/roBOT/blob/master/docs/COMMANDS.md \
        to know all commands I understand. \nI hope you're still here. Looking forward to spend some quality time with you.  \
        \nTo know how you can improve my functionality use  '_contribute' ",
        color=discord.Color.blue(),
    )
    await message.channel.send(embed=embed)
    await message.add_reaction("\U0001f44d")


async def contrib(discord, message):
    embed = discord.Embed(
        title="Interested about open-source contribution ? ",
        description="Looks like you're interested to help my fellow amatuer creators in order to make\
            myself more polished and funky !!\n Here's the link to repo: https://github.com/danger-ahead/roBOT\
                \n Feel free to give your suggestion as issues and submit PR requests with improvements!!\
                \n waiting for you PR peeps!! ",
        color=discord.Color.blue(),
    )
    await message.channel.send(embed=embed)
    await message.add_reaction("\U0001f44d")
