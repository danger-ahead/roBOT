import datetime
import discord
from discord.ext import commands
from typing import Optional

class PlayFlags(commands.FlagConverter, delimiter=' ', prefix='-'):
    direct: Optional[str] = commands.flag(name="direct", aliases=['dir','d'])

class Playdown(discord.ui.Select):
    def __init__(self, *options):

        super().__init__(
            row=0,
            placeholder="Select what you want to do",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        assert self.view is not None
        view: playView = self.view
        view.option = self.values[0]


class playView(discord.ui.View):
    def __init__(self, timeout: Optional[float] = 180):
        self.option = None
        self.toStop = True
        self.activity_type = {
            "755600276941176913": "YOUTUBE",
            "755827207812677713": 'POKER',
            "773336526917861400": 'BETRAYAL',
            "814288819477020702": 'FISHING',
            "832012774040141894": 'CHESS'
        }  
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, row=1)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.option==None:
            embed = discord.Embed(color=0xFF0000, title="⛔ Error", description="You need to chhose one select option in order to start the activity.")
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(ephemeral=True, embed=embed)
        else:
            try:
                invite = await self.voice_state.channel.create_invite(
                    max_age=86400,
                    target_type=discord.InviteTarget.embedded_application,
                    target_application_id = int(self.option)
                )
            except discord.errors.Forbidden:
                embed = discord.Embed(color=0xFF0000, title="⛔ Error", description="Bot is missing required `Create Instant Invite` permission to run this command")
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                await self.message.delete()
                self.toStop = False
                self.stop()
            else:
                embed = discord.Embed(title="Discord Embeded Application", description=f"Click the button to start your {self.activity_type[self.option]} activity in **{self.voice_state.channel.name}**", color=0x2F3136)
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.timestamp = datetime.datetime.now()
                view=discord.ui.View(timeout=0)
                view.add_item(discord.ui.Button(label="Start Activity", url=invite.url))
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(embed=embed, view=view)
                self.toStop = False
                await self.message.delete()
                self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, row=1)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.message.delete()
        self.toStop = False
        self.stop()

    async def on_timeout(self):
        if self.toStop:
            for i in range(len(self.children)):
                self.children[i].disabled=True
            await self.message.edit(view=self)

class PlayGames(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.application_ids = {
            "YOUTUBE": ["755600276941176913", "Youtube Go"],
            'POKER': ["755827207812677713", "Poker Night"],
            'BETRAYAL': ["773336526917861400", "Betrayal.io"],
            'FISHING': ["814288819477020702", "Fishington.io"],
            'CHESS': ["832012774040141894", "Chess In The Park"]
        }   

    @commands.command(aliases=["pt"])
    @commands.guild_only()
    async def playtogether(self, ctx, *, messageFlag: PlayFlags):
        voice_state = ctx.author.voice
        if voice_state==None:
            await ctx.send("You need to be in a vc to use this command")
            return
        
        if messageFlag.direct==None:
            options = []
            for key, value in self.application_ids.items():
                options.append(discord.SelectOption(label=value[1], value=value[0], description=f"Start the {key} activity."))
            view = playView()
            view.voice_state = voice_state
            view.client = self.client
            view.add_item(Playdown(*options))
            embed = discord.Embed(title="Discord Embeded Application", description="Choose an option to start a discord embeded application activity", color=0x2F3136)
            embed.set_thumbnail(url=self.client.user.avatar.url)
            embed.timestamp = datetime.datetime.now()
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            view.message = await ctx.send(content="Waiting for you to click the confirm",embed=embed, view=view)
        else:
            if messageFlag.direct.upper() in self.application_ids.keys():
                option = self.application_ids[messageFlag.direct.upper()][0]
                try:
                    invite = await voice_state.channel.create_invite(
                        max_age=86400,
                        target_type=discord.InviteTarget.embedded_application,
                        target_application_id = int(option)
                    )
                except discord.errors.Forbidden:
                    embed = discord.Embed(color=0xFF0000, title="⛔ Error", description="Bot is missing required `Create Instant Invite` permission to run this command")
                    embed.set_thumbnail(url=self.client.user.avatar.url)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Discord Embeded Application", description=f"Click the button to start the activity in {voice_state.channel.name}", color=0x2F3136)
                    embed.set_thumbnail(url=self.client.user.avatar.url)
                    embed.timestamp = datetime.datetime.now()
                    view=discord.ui.View(timeout=0)
                    view.add_item(discord.ui.Button(label="Start Activity", url=invite.url))
                    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                    await ctx.send(embed=embed, view=view)
            else:
                embed = discord.Embed(color=0xFF0000, title="⛔ Error", description="We only provide `Youtube`, `Poker`, `Chess`, `Fishing`, `Betrayal`.\nPlease choose in between these")
                embed.set_thumbnail(url=self.client.user.avatar.url)
                embed.timestamp = datetime.datetime.now()
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PlayGames(client))
