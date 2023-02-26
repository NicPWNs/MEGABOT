#!/usr/bin/env python3
import time
import discord
import yt_dlp


async def play(ctx, search):

    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")

    ydl_opts = {
        'quiet': True,
        'outtmpl': "media/%(id)s",
        'default_search': 'ytsearch',
        'format': 'bestaudio/best',
        'prefer_ffmpeg': True,
        'force_overwrites': True,
        'nocheckcertificate': True,
        'no_warnings': True,
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    channel = ctx.author.voice.channel
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    ctx.voice_client.stop()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url=search, download=False)
        url = info["entries"][0]["formats"][0]['url']

        source = await discord.FFmpegOpusAudio.from_probe(source=url, method='fallback', **FFMPEG_OPTIONS)
        voice.play(source)
        voice.is_playing()
