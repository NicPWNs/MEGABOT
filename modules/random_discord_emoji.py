import discord
from random_unicode_emoji import random_emoji


async def random_discord_emoji(guild, bot, discordName):

    guild = discord.utils.get(bot.guilds, name=discordName)
    emojis = await guild.fetch_emojis()

    # Remove playing card emojis
    emojis = list(
        filter(lambda a: (len(a.name) == 2 or len(a.name) == 3) and a.name[-1] not in ['c', 'd', 'h', 's'], emojis))

    # Increase ratio of Discord emojis
    for _ in range(0, 6):
        emojis = emojis + emojis

    return random_emoji(version="15.0", custom=emojis)[0]
