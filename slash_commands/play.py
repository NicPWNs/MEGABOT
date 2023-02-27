#!/usr/bin/env python3
import json
import discord
from yt_dlp import YoutubeDL


async def play(ctx, search):

    await ctx.respond(content="*⏳ Loading...*")

    ytdlOpts = {
        'quiet': True,
        'outtmpl': "media/%(id)s",
        'default_search': 'ytsearch',
        'no_post_overwrites': True,
        'no-part': True,
        'format': 'bestaudio/best',
        'prefer_ffmpeg': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ytdlOpts) as ytdl:
        info = ytdl.extract_info(search, download=False)

    ytdlOpts['download_archive'] = 'downloaded.txt'

    with YoutubeDL(ytdlOpts) as ytdl:
        ytdl.download(search)

    channel = ctx.author.voice.channel
    voice = await channel.connect()

    voice.play(discord.FFmpegPCMAudio(source=f"media/{id}.mp3"))
    voice.source = discord.PCMVolumeTransformer(
        original=voice.source, volume=0.075)

    id = info["entries"][0]["id"]

    content = f"Playing!"

    await ctx.edit(content=content)
