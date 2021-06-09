async def _create_poll(discord, message):
    content = message.content[message.content.find(' '):]
    content_list = content.split(',,')
    emoji = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

    if len(content_list) > 10:
        await message.channel.send('Can\'t create a poll with more than 9 options')
    else:
        await message.delete()
        option=''
        for i in range(1, len(content_list)):
            option+=emoji[i-1]+content_list[i]+'\n'

        embed=discord.Embed(title='Poll: '+content_list[0],
        description=option+'\nBy <@'+str(message.author.id)+'>', color=discord.Color.blue())

        try:
            embed_message=await message.channel.send(embed=embed)
            for i in range(len(content_list)-1):
                await embed_message.add_reaction(emoji[i])

        except:
            await message.channel.send('Error!!\n\
            You can try reducing the no. of characters in the poll.')
