#!/usr/bin/env python3
import os
import discord
import spotdl
import asyncio
import nest_asyncio


nest_asyncio.apply()


async def spot(ctx, search, queue):

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

    sdl = spotdl.Spotdl(client_id=str(os.getenv('SPOTIFY_CLIENT')), client_secret=str(os.getenv('SPOTIFY_SECRET')), downloader_settings=None, headless=True, loop=asyncio.get_event_loop())
    song = sdl.search([search])[0]
    title = song.name
    cover = song.cover_url
    song, path = sdl.download(song)

    channel = ctx.author.voice.channel

    try:
        voice = await channel.connect()
    except:
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        await voice.move_to(channel)

    try:
        voice.play(discord.FFmpegPCMAudio(source=path))
        voice.source = discord.PCMVolumeTransformer(original=voice.source, volume=0.25)
    except:
        pass

    embed = discord.Embed(color=0x5daced,
                          title="🎵  Now Playing",
                          description=f"{title}"
                        ).set_thumbnail(url=cover)

    await interaction.edit_original_response(embed=embed)
