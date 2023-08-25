#!/usr/bin/env python3
import os
import re
import shutil
import random
import discord
import requests
import asyncio
from difflib import SequenceMatcher
from colorthief import ColorThief


async def album(ctx, genre="hip-hop"):

    def check(msg):
        return msg.author.id == ctx.user.id

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

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

    while artist == "Various Artists":
        album = requests.get(
            f'https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track&market=NA&limit=1&offset={str(random.randint(0, 350))}', headers=headers).json()['tracks']['items'][0]['album']
        cover = album['images'][0]['url']
        artist = album['artists'][0]['name']

    with open("cover.jpg", 'wb') as f:
        shutil.copyfileobj(requests.get(cover, stream=True).raw, f)
    color = ColorThief("./cover.jpg")
    color = int('%02x%02x%02x' % color.get_color(quality=1), 16)

    embed = discord.Embed(color=color,
                          title="💽  Guess the Artist of this Album Cover!"
                          ).set_image(url=cover)

    await interaction.edit_original_response(embed=embed)

    try:
        msg = await ctx.bot.wait_for("message", timeout=60, check=check)
    except asyncio.TimeoutError:
        text = f"❌ {ctx.user.name} did not guess within 60 seconds!"

        embed = discord.Embed(color=color,
                              title="💽  Guess the Artist of this Album Cover!"
                              ).set_image(url=cover).set_footer(text=text, icon_url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return
    await msg.delete()

    text = f"❌ {ctx.user.name} is Incorrect! The artist is {artist}"

    guess = re.sub("[^A-Z]", "", msg.content.lower(), 0, re.IGNORECASE)
    answer = re.sub("[^A-Z]", "", artist.lower(), 0, re.IGNORECASE)

    if SequenceMatcher(a=guess, b=answer).ratio() >= 0.9:
        text = f"✅ {ctx.user.display_name} is Correct! The artist is {artist}"

    embed = discord.Embed(color=color,
                          title="💽  Guess the Artist of this Album Cover!"
                          ).set_image(url=cover).set_footer(text=text, icon_url=ctx.user.display_avatar)

    await interaction.edit_original_response(embed=embed)

    os.remove("./cover.jpg")
