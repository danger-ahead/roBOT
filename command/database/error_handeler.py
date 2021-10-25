import discord
import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, discord.Forbidden, commands.NotOwner, discord.HTTPException, discord.NotFound, discord.errors.Forbidden, commands.errors.CheckAnyFailure, discord.ext.flags._parser.ArgumentParsingError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        
        elif isinstance(error, commands.PrivateMessageOnly):
            try:
                await ctx.author.send(f'{ctx.command} can only be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            await ctx.send('I could not understand the value you had put. Please try again.')
        
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.send('I could not understand the value you had put. Please try again.')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You are missing few arguements. Please check the help to know more about specific arguement.')

        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send('I could not understand the value you had put. Please try again.')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'You are missing **{",".join([perm for perm in error.missing_perms])}** permission to run this command.')
        
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'I are missing **{",".join([perm for perm in error.missing_perms])}** permission to run this command.')

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Retry after {error.retry_after} seconds...')

        # All the list of errors are written in https://pycord.readthedocs.io/en/stable/api.html#exceptions
        # And they can be added to be handeled in elif after this line
        

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(client):
    client.add_cog(CommandErrorHandler(client))