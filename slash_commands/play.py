#!/usr/bin/env python3
import re
import discord
from yt_dlp import YoutubeDL


ytdlOpts = {
    'quiet': True,
    'outtmpl': "media/%(id)s",
    'default_search': 'ytsearch',
    'no_post_overwrites': True,
    'no_part': True,
    'format': 'bestaudio/best',
    'prefer_ffmpeg': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


async def play(ctx, search, queue):

    info = {}

    response = await ctx.respond(content="*⏳ Loading...*")

    if not ctx.author.voice:
        await ctx.edit(content=f"**❌  <@{ctx.user.id}> is not connected to a voice channel!**")
        return

    channel = ctx.author.voice.channel
    voice = await channel.connect()

    with YoutubeDL(ytdlOpts) as ytdl:
        info = ytdl.extract_info(search, download=False)

    id = info["entries"][0]["id"]
    title = info["entries"][0]["title"]

    title = re.sub("\[.*\]", "", title)

    voice.play(discord.FFmpegPCMAudio(source=getSource(search, id)))
    voice.source = discord.PCMVolumeTransformer(
        original=voice.source, volume=0.25)

    embed = discord.Embed(color=0x5daced,
                          title=f"🎵  Now Playing",
                          description=f"{title}"
                        )

    await response.edit(embed=embed)


def getSource(search, id):

    ytdlOpts['download_archive'] = 'downloaded.txt'

    with YoutubeDL(ytdlOpts) as ytdl:
        ytdl.download(search)

    source = f"media/{id}.mp3"

    del ytdlOpts['download_archive']

    return source
