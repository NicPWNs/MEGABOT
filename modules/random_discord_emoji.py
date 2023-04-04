import discord
from random_unicode_emoji import random_emoji


async def random_discord_emoji(guild, bot, discordName):

    guild = discord.utils.get(bot.guilds, name=discordName)
    emojis = await guild.fetch_emojis()

    # Increase ratio of Discord emojis
    for _ in range(0, 6):
        emojis = emojis + emojis

    # Remove playing card emojis
    for emoji in emojis:
        if len(emoji.name) == 2 and emoji.name[1] in ['c', 'd', 'h', 's']:
            emojis.remove(emoji)

    return random_emoji(version="14.0", custom=emojis)[0]
