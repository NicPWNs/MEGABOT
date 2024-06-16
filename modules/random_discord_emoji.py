import discord
from random_unicode_emoji import random_emoji


async def random_discord_emoji(guild, bot, discordName):

    guild = discord.utils.get(bot.guilds, name=discordName)
    emojis = await guild.fetch_emojis()

    # Remove playing card emojis
    faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
    suits = ["c", "d", "h", "s"]
    cards = []
    for shape in faces:
        for color in suits:
            cards.append(shape + color)

    emojis = [x for x in emojis if x.name not in cards]

    # Increase ratio of Discord emojis
    for _ in range(0, 6):
        emojis = emojis + emojis

    return random_emoji(version="15.0", custom=emojis)[0]
