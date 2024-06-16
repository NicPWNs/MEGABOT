#!/usr/bin/env python3
import os
import re

import discord
import asyncio
import ffmpeg
import spotdl
import requests
from yt_dlp import YoutubeDL


async def queuer(ctx, queued, played, interaction, embed):

    await interaction.edit_original_response(embed=embed)
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    voice.stop()

    if len(queued) == 0:
        embed = discord.Embed(color=0x5DACED, title="☑️  Queue Complete")
        await ctx.channel.send(embed=embed)
        await voice.disconnect()

    while len(queued) > 0:
        voice.play(discord.FFmpegPCMAudio(source=queued[0]))
        voice.source = discord.PCMVolumeTransformer(original=voice.source, volume=0.25)
        length = float(ffmpeg.probe(queued[0])["format"]["duration"])
        played.insert(0, queued[0])
        queued.pop(0)
        await asyncio.sleep(length)


async def play(ctx, search, queued, played, SDL, skip, replay):

    if skip:
        embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
        interaction = await ctx.respond(embed=embed)

        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if not voice:
            embed = discord.Embed(
                color=0xDD2F45, title="❌  MEGABOT Is Not In Voice"
            ).set_thumbnail(
                url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif"
            )
            await interaction.edit_original_response(embed=embed)

        else:
            embed = discord.Embed(color=0x5DACED, title="⏭️  Skipping Song!")
            await queuer(ctx, queued, played, interaction, embed)

    elif replay:
        embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
        interaction = await ctx.respond(embed=embed)

        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if not voice:
            embed = discord.Embed(
                color=0xDD2F45, title="❌  MEGABOT Is Not In Voice"
            ).set_thumbnail(
                url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif"
            )
            await interaction.edit_original_response(embed=embed)

        else:
            embed = discord.Embed(color=0x5DACED, title="🔁  Replaying Current Song!")
            await interaction.edit_original_response(embed=embed)
            queued.insert(0, played[0])

    else:
        embed = discord.Embed(
            color=0xFEE9B6,
            title="⏳  Downloading...",
            description=f'**Request:** "{search}"',
        )

        interaction = await ctx.respond(embed=embed)

        if not ctx.author.voice:
            embed = discord.Embed(
                color=0xDD2F45,
                title="❌  Error",
                description=f"<@{ctx.user.id}> is not connected to a voice channel!",
            ).set_thumbnail(url=ctx.user.display_avatar)

            await interaction.edit_original_response(embed=embed)
            return

        channel = ctx.author.voice.channel

        try:
            voice = await channel.connect()
        except:
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            await voice.move_to(channel)

        if "http" in search:
            if bool(re.search(r"https:\/\/www\.youtube\.com\/.*", search)):
                ydl_opts = {
                    "skip_download": True,
                    "noplaylist": True,
                    "quiet": True,
                    "no_warnings": True,
                    "get_title": True,
                }

                with YoutubeDL(ydl_opts) as ydl:
                    search = ydl.extract_info(search, download=False, process=False)[
                        "title"
                    ]
            elif bool(re.search(r"https:\/\/open\.spotify\.com\/.*", search)):
                pass
            elif bool(re.search(r"https:\/\/tidal\.com\/.*", search)):
                re_match = re.search(r"https:\/\/tidal\.com\/.*\/(\d*)", search)
                if re_match:
                    tidal_id = re_match.group(1)

                data = {"grant_type": "client_credentials"}
                r = requests.post(
                    "https://auth.tidal.com/v1/oauth2/token",
                    auth=requests.auth.HTTPBasicAuth(
                        os.getenv("TIDAL_CLIENT"), os.getenv("TIDAL_SECRET")
                    ),
                    data=data,
                ).json()
                bearer = "Bearer " + r["access_token"]

                headers = {
                    "Authorization": bearer,
                    "Content-Type": "application/vnd.tidal.v1+json",
                }

                r = requests.get(
                    f"https://openapi.tidal.com/tracks/{tidal_id}?countryCode=US",
                    headers=headers,
                ).json()

                search = r["resource"]["title"] + r["resource"]["artists"][0]["name"]

            else:
                embed = discord.Embed(
                    color=0xDD2F45,
                    title="❌  Error",
                    description=f"Only **YouTube**, **Spotify**, and **TIDAL** URLs are currently supported!",
                ).set_thumbnail(url=ctx.user.display_avatar)
                await interaction.edit_original_response(embed=embed)
                return

        try:
            song = SDL.search([search])[0]
            title = song.name
            cover = song.cover_url
            artist = song.artist
            song, path = SDL.download(song)
            queued.append(path)

        except spotdl.types.song.SongError:
            embed = discord.Embed(
                color=0xDD2F45,
                title="❌  Error",
                description=f"**No results found for:** {search}",
            ).set_thumbnail(url=ctx.user.display_avatar)
            await interaction.edit_original_response(embed=embed)
            return

        embed = (
            discord.Embed(
                color=0x5DACED, title="🎵  Now Playing", description=f"{title}"
            )
            .set_thumbnail(url=cover)
            .set_footer(text=f"by {artist}")
        )

        if not voice.is_playing():
            await queuer(ctx, queued, played, interaction, embed)
        else:
            embed = (
                discord.Embed(
                    color=0x5DACED, title="↩️  Added to Queue", description=f"{title}"
                )
                .set_thumbnail(url=cover)
                .set_footer(text=f"by {artist}")
            )

            await interaction.edit_original_response(embed=embed)
