"""
Module containing functions for all the admin commands.
"""

from commands.scripts import loader


async def clean(message):
    await message.channel.purge(limit=100)


async def configure(message):
    db = loader.db_loaded()
    await db.server_config(message.guild.id, message)


async def deconfigure(message):
    db = loader.db_loaded()
    await db.server_deconfig(message.guild.id, message)


async def leave(message):
    db = loader.db_loaded()
    await db.leave_server(message.guild.id, message)


async def moderation(message):
    db = loader.db_loaded()
    await db.moderation_service(message.guild.id, message)


async def kick(message):
    db = loader.db_loaded()
    if message.mentions.__len__() > 0:
        for user in message.mentions:
            user = await message.guild.query_members(user_ids=[user.id])
        user = user[0]
        await user.kick(reason="Kicked by roBOT!")


async def mute(message):
    db = loader.db_loaded()
    if message.mentions.__len__() > 0:
        for user in message.mentions:
            user = await message.guild.query_members(user_ids=[user.id])
        user = user[0]

        try:
            await user.edit(mute=True)
        except Exception:
            await message.channel.send("User's not connected to voice!")


async def unmute(message):
    db = loader.db_loaded()
    if message.mentions.__len__() > 0:
        for user in message.mentions:
            user = await message.guild.query_members(user_ids=[user.id])
        user = user[0]
        try:
            await user.edit(mute=False)
        except Exception:
            await message.channel.send("User's not connected to voice!")


async def configconfess(message):
    db = loader.db_loaded()
    await db.confess_config(message.guild.id, message)


async def deconfigconfess(message):
    db = loader.db_loaded()
    await db.confess_deconfig(message.guild.id, message)
