"""
Module containing the functions for _confess and _rank commands.
"""

from commands.scripts import loader


async def confess(discord, message):
    await message.delete()
    db = loader.db_loaded()
    client = loader.client_loaded()
    hold = message.content.find(" ")  # searches for the first space after the command
    await db.confess(
        client,
        discord,
        message.content[(hold + 1) : len(message.content)],
        message,
    )


async def rank(discord, message):
    db = loader.db_loaded()
    await db.rank_query(message)
    await message.add_reaction("\U0001f44d")
