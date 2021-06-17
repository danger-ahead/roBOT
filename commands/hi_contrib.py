async def hi(discord, message):
    embed = discord.Embed(
        title="Hello comrade!!, Meet myself roBOT!",
        description="an amatuer bot by amatuer Developers!! XD \
        \n The full list of commands \
        can be found here: \n https://github.com/RccTechz/roBOT/blob/master/docs/COMMANDS.md \n\
        have a great time interacting and having fun with me!!\n for details about how to contribute to \
        this bot use  '_contribute' ",
        color=discord.Color.blue(),
    )
    await message.channel.send(embed=embed)


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
