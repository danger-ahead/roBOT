from commands.scripts import loader

async def confess(discord, message):
    await message.delete()
    db = loader.db_loaded()
    client = loader.client_loaded()
    hold = message.content.find(
        " "
    )  # searches for the first space after the command
    await db.confess(
        client,
        discord,
        message.content[(hold + 1) : len(message.content)],
        message,
    )