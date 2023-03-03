#!/usr/bin/env python3
import re
import time
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
    'extact_audio': True,
    'audio_format': "mp3",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


async def play(ctx, search, queue):

    embed = discord.Embed(color=0xfee9b6,
                        title="⏳  Searching...",
                        description=f"**Request:** \"{search}\""
                        )

    interaction = await ctx.respond(embed=embed)

    if not ctx.author.voice:
        embed = discord.Embed(color=0xdd2f45,
                          title="❌  Error",
                          description=f"<@{ctx.user.id}> is not connected to a voice channel!"
                        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    info = YoutubeDL(ytdlOpts).extract_info(search, download=False)
    ytdlOpts['download_archive'] = 'downloaded.txt'

    id = info["entries"][0]["id"]
    title = re.sub("\[.*\]", "", info["entries"][0]["title"])
    title = re.sub("\(.*\)", "", title)
    thumbnail = info["entries"][0]["thumbnail"]
    source = f"media/{id}.mp3"

    if id not in open("downloaded.txt").read():
        embed = discord.Embed(color=0x77b354,
                          title="📥  Downloading...",
                          description=f"\"{title}\" is a new request."
                        ).set_thumbnail(url=thumbnail) \
                         .set_footer(text="Please be patient")

        await interaction.edit_original_response(embed=embed)

    YoutubeDL(ytdlOpts).download(search)
    ytdlOpts.pop('download_archive')

    channel = ctx.author.voice.channel

    try:
        voice = await channel.connect(timeout=600.0)
    except:
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await voice.move_to(channel)
    time.sleep(1)

    try:
        voice.play(discord.FFmpegPCMAudio(source=source))
        voice.source = discord.PCMVolumeTransformer(
            original=voice.source, volume=0.25)
    except:
        pass

    embed = discord.Embed(color=0x5daced,
                          title="🎵  Now Playing",
                          description=f"{title}"
                        ).set_thumbnail(url=thumbnail)

    await interaction.edit_original_response(embed=embed)
