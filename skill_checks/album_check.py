#!/usr/bin/env python3
import os
import re
import math
import shutil
import random
import discord
import requests
import asyncio
from difflib import SequenceMatcher
from colorthief import ColorThief

import megacoin


async def album_check(bot, genre="hip-hop"):

    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="main")

    def check(msg):
        guess = re.sub("[^A-Z]", "", msg.content.lower(), 0, re.IGNORECASE)
        answer = re.sub("[^A-Z]", "", artist.lower(), 0, re.IGNORECASE)
        if SequenceMatcher(a=guess, b=answer).ratio() >= 0.9:
            return True

    data = {
        'grant_type': 'client_credentials',
        'client_id': str(os.getenv('SPOTIFY_CLIENT')),
        'client_secret': str(os.getenv('SPOTIFY_SECRET'))
    }

    token = requests.post(
        'https://accounts.spotify.com/api/token', data=data).json()['access_token']

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    artist = "Various Artists"
    type = "single"

    while artist == "Various Artists" and type == "single":
        track = requests.get(
            f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=NA&limit=1&offset={str(random.randint(0, 350))}', headers=headers).json()['tracks']['items'][0]
        cover = track['album']['images'][0]['url']
        artist = track['album']['artists'][0]['name']
        type = track['album']['album_type']
        popularity = track['popularity']

    with open("cover.jpg", 'wb') as f:
        shutil.copyfileobj(requests.get(cover, stream=True).raw, f)
    color = ColorThief("./cover.jpg")
    color = int('%02x%02x%02x' % color.get_color(quality=1), 16)

    coins = math.ceil(((100 - popularity) * 4) * .1)

    embed = discord.Embed(color=color,
                          title="💽  Guess the Artist of this Album Cover",
                          description=f"Anyone can answer within 5 minutes for <:MEGACOIN:1090620048621707324> *x{coins}*"
                          ).set_image(url=cover).set_author(name="🎯  Skill Check!")

    message = await channel.send(embed=embed)

    try:
        msg = await bot.wait_for("message", timeout=300, check=check)
    except asyncio.TimeoutError:
        text = f"❌ No one guessed correctly within 5 minutes!"

        embed = embed.set_footer(
            text=text, icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/thumbnail.gif")

        await message.edit(embed=embed)
        return

    await msg.add_reaction("✅")
    text = f"✅ {msg.author.name} Wins! The artist is {artist}"
    await megacoin.add(msg.author, coins)

    embed = embed.set_footer(text=text, icon_url=msg.author.display_avatar)

    await message.edit(embed=embed)

    os.remove("./cover.jpg")
