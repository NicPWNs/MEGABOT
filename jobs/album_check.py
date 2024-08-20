#!/usr/bin/env python3
import os
import re
import math
import time
import shutil
import discord
import requests
import asyncio
import modules.megacoin as megacoin
from difflib import SequenceMatcher
from colorthief import ColorThief


async def album_check(bot, startTime):

    runTime = int(time.time() - startTime)
    if runTime < 60:
        return

    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="casino")

    def check(msg):
        if msg.channel == channel:
            guess = re.sub("[^A-Z]", "", msg.content.lower(), 0, re.IGNORECASE)
            answer = re.sub("[^A-Z]", "", artist.lower(), 0, re.IGNORECASE)
            if SequenceMatcher(a=guess, b=answer).ratio() >= 0.9:
                return True

    data = {
        "grant_type": "client_credentials",
        "client_id": str(os.getenv("SPOTIFY_CLIENT")),
        "client_secret": str(os.getenv("SPOTIFY_SECRET")),
    }

    token = requests.post("https://accounts.spotify.com/api/token", data=data).json()[
        "access_token"
    ]

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
    }

    # Configure genre here
    genre = "hip-hop"

    track = requests.get(
        f"https://api.spotify.com/v1/recommendations?limit=1&market=NA&seed_genres={genre}",
        headers=headers,
    ).json()["tracks"][0]
    cover = track["album"]["images"][0]["url"]
    artist = track["album"]["artists"][0]["name"]
    popularity = track["popularity"]

    with open("cover.jpg", "wb") as f:
        shutil.copyfileobj(requests.get(cover, stream=True).raw, f)
    color = ColorThief("./cover.jpg")
    color = int("%02x%02x%02x" % color.get_color(quality=1), 16)

    coins = math.ceil(((100 - popularity) * 4) * 0.1)

    embed = (
        discord.Embed(
            color=color,
            title="💽  Guess the Artist of this Album Cover",
            description=f"Anyone can answer within 10 minutes for <:MEGACOIN:1090620048621707324> *x{coins}*",
        )
        .set_image(url=cover)
        .set_author(name="🎯  Skill Check!")
    )

    try:
        message = await channel.send(embed=embed)
    except discord.errors.Forbidden:
        return

    try:
        msg = await bot.wait_for("message", timeout=600, check=check)
    except asyncio.TimeoutError:
        text = f"❌ No one guessed correctly within 10 minutes!"

        embed = embed.set_footer(
            text=text,
            icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif",
        )

        await message.edit(embed=embed)
        return

    await msg.add_reaction("✅")
    text = f"+ {coins} ✅ {msg.author.display_name} Wins! The artist is {artist}"
    await megacoin.add(msg.author, coins)

    embed = embed.set_footer(
        text=text,
        icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png",
    )
    await message.edit(embed=embed)

    os.remove("./cover.jpg")
