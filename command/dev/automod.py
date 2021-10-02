from discord.ext import commands


class AutoMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.path = "./command/dev/moderate.txt"

    # a method to return gae words in moderate.txt file
    def filter(self):
        with open(self.path) as file:
            data = file.read().split('\n')
            return data

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content in AutoMod.filter(self):
            await message.channel.send(f"You're being warned {message.author.mention}")


def setup(client):
    client.add_cog(AutoMod(client))