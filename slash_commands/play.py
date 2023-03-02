#!/usr/bin/env python3
import re
import json
import discord
from yt_dlp import YoutubeDL


ytdlOpts = {
    'quiet': True,
    'outtmpl': "media/%(id)s",
    'default_search': 'ytsearch',
    'no_post_overwrites': True,
    'no_part': True,
    # 'download_archive': 'downloaded.txt',
    'format': 'bestaudio/best',
    'prefer_ffmpeg': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


async def play(ctx, search, queue):

    info = {}

    embed = discord.Embed(color=0xfee9b6,
                        title="⏳  Searching...",
                        description=f"**Request:** {search}"
                        )

    interaction = await ctx.respond(embed=embed)

    if not ctx.author.voice:
        embed = discord.Embed(color=0xdd2f45,
                          title="❌  Error",
                          description=f"<@{ctx.user.id}> is not connected to a voice channel!"
                        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    channel = ctx.author.voice.channel
    try:
        voice = await channel.connect()
    except:
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await voice.move_to(channel)

    with YoutubeDL(ytdlOpts) as ytdl:
        info = ytdl.extract_info(search, download=False)

    id = info["entries"][0]["id"]
    title = info["entries"][0]["title"]
    thumbnail = info["entries"][0]["thumbnail"]
    url = info["entries"][0]["formats"][0]['url']
    source = f"media/{id}.mp3"

    title = re.sub("\[.*\]", "", title)

    source = await discord.FFmpegOpusAudio.from_probe(source=url, **FFMPEG_OPTS)
    voice.play(source)
    # voice.source = discord.PCMVolumeTransformer(
    #     original=voice.source, volume=0.25)

    embed = discord.Embed(color=0x5daced,
                          title="🎵  Now Playing",
                          description=f"{title}"
                        ).set_thumbnail(url=thumbnail)

    await interaction.edit_original_response(embed=embed)
