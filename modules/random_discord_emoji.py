import discord
from random_unicode_emoji import random_emoji

# Get random emoji including custom discord emojis
async def random_discord_emoji(guild, bot, discordName):
    
    guild = discord.utils.get(bot.guilds, name=discordName)
    emojis = await guild.fetch_emojis()
    for _ in range(0, 6):
        emojis = emojis + emojis


    return random_emoji(version="14.0", custom=emojis)[0]
