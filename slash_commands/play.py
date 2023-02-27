#!/usr/bin/env python3
import json
import discord
from yt_dlp import YoutubeDL


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


async def play(ctx, search, queue, stop):

    await ctx.respond(content="*⏳ Loading...*")

    if stop:
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        content = f"**🔇  Music Stopped!**"
        await ctx.edit(content=content)
        return

    channel = ctx.author.voice.channel
    voice = await channel.connect()

    with YoutubeDL(ytdlOpts) as ytdl:
        info = ytdl.extract_info(search, download=False)

    id = info["entries"][0]["id"]
    title = info["entries"][0]["title"]

    voice.play(discord.FFmpegPCMAudio(source=getSource(search, id)))
    voice.source = discord.PCMVolumeTransformer(
        original=voice.source, volume=0.1)

    content = f"**🎵  Playing `{title}`**"

    await ctx.edit(content=content)


def getSource(search, id):

    ytdlOpts['download_archive'] = 'downloaded.txt'

    with YoutubeDL(ytdlOpts) as ytdl:
        ytdl.download(search)

    source = f"media/{id}.mp3"

    return source
