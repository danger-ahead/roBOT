import asyncio

class Poll:
    """
    Class for creating and checking the results of polls
    """
    def __init__(self):
        self.emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        self.content = ''
        self.content_list = []
        print('Running: Poll module [poll.py]\n')

#creates the template of the pole and sends the embed to channel
    async def _create_poll(self, discord, message):
        self.content = message.content[message.content.find(' '):]
        self.content_list = self.content.split(',,')

        #1 topic + 9 choices + 1 duration = 11
        if len(self.content_list) > 11:
            await message.channel.send('Can\'t create a poll with more than 9 choices!')
        else:
            option = ''
            #stores all the choices with the corresponding emoji
            for i in range(1, len(self.content_list)-1):
                option += self.emoji[i-1]+self.content_list[i]+'\n'

            embed = discord.Embed(title='Poll: '+self.content_list[0],
            description = option+'\nBy <@'+str(message.author.id)+'>', color=discord.Color.blue())

            try:
                embed_message = await message.channel.send(embed=embed)
                #add reactions to roBOT's own poll message
                for i in range(len(self.content_list)-2):
                    await embed_message.add_reaction(self.emoji[i])

                #checks if user has provided poll duration
                try:
                    await asyncio.sleep(float(self.content_list[len(self.content_list)-1])*60+5)
                    await self._count_votes(discord, message, embed_message)
                except:
                    await message.channel.send('<@'+str(message.author.id)+'>'+' provide poll duration!')
                    await embed_message.delete()
            except:
                await message.channel.send('Error! :/')

#function to check for reactions after poll duration is over
    async def _count_votes(self, discord, message, embed_message):
        cache_msg = await message.channel.fetch_message(embed_message.id)
        store_reaction = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        total = ''

        #checks and stores when particular reaction's count goes above 1
        for i in range(len(self.content_list)-2):
            reaction = discord.utils.get(cache_msg.reactions, emoji=self.emoji[i])
            if reaction and reaction.count > 1:
                store_reaction[i] = reaction.count

        max_value = max(store_reaction)
        if max_value != 1:
            #stores the maximum voted choice(s)
            for i in range(len(store_reaction)):
                if store_reaction[i] == max_value:
                    total += self.emoji[i] + ' , '

            embed = discord.Embed(title='Poll results',
            description=total[:len(total)-3]+' got the maximum votes!', color=discord.Color.blue())
            await embed_message.reply(embed=embed)
        else:
            await embed_message.reply('No votes were cast!')
