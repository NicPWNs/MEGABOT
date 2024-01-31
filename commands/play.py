#!/usr/bin/env python3
import re
import discord
import asyncio
import ffmpeg
import spotdl
from yt_dlp import YoutubeDL


async def queuer(ctx, queued, interaction, embed):

    await interaction.edit_original_response(embed=embed)
    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    voice.stop()

    if len(queued) == 0:
        embed = discord.Embed(color=0x5daced, title="☑️  Queue Complete")
        await ctx.channel.send(embed=embed)
        await voice.disconnect()

    while len(queued) > 0:
        voice.play(discord.FFmpegPCMAudio(source=queued[0]))
        voice.source = discord.PCMVolumeTransformer(
            original=voice.source, volume=0.25)
        length = float(ffmpeg.probe(queued[0])['format']['duration'])
        queued.pop(0)
        await asyncio.sleep(length)


async def play(ctx, search, queued, SDL, skip):

    if skip:
        embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
        interaction = await ctx.respond(embed=embed)

        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if not voice:
            embed = discord.Embed(color=0xdd2f45, title="❌  MEGABOT Is Not In Voice").set_thumbnail(
                url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif")
            await interaction.edit_original_response(embed=embed)

        else:
            embed = discord.Embed(color=0x5daced, title="⏭️  Skipping Song!")
            await queuer(ctx, queued, interaction, embed)

    else:
        embed = discord.Embed(color=0xfee9b6,
                              title="⏳  Downloading...",
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

        channel = ctx.author.voice.channel

        try:
            voice = await channel.connect()
        except:
            voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            await voice.move_to(channel)

        if "http" in search:
            if bool(re.search(r"https:\/\/www\.youtube\.com\/.*", search)):
                ydl_opts = {
                    'skip_download': True,
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'get_title': True
                }

                with YoutubeDL(ydl_opts) as ydl:
                    search = ydl.extract_info(
                        search, download=False, process=False)['title']
            elif bool(re.search(r"https:\/\/open\.spotify\.com\/.*", search)):
                pass
            else:
                embed = discord.Embed(color=0xdd2f45,
                                      title="❌  Error",
                                      description=f"Only **YouTube** and **Spotify** URLs are Currenty Supported!"
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
            embed = discord.Embed(color=0xdd2f45,
                                  title="❌  Error",
                                  description=f"**No results found for:** {search}"
                                  ).set_thumbnail(url=ctx.user.display_avatar)
            await interaction.edit_original_response(embed=embed)
            return

        embed = discord.Embed(color=0x5daced,
                              title="🎵  Now Playing",
                              description=f"{title}"
                              ).set_thumbnail(url=cover).set_footer(text=f"by {artist}")

        if not voice.is_playing():
            await queuer(ctx, queued, interaction, embed)
        else:
            embed = discord.Embed(color=0x5daced,
                                  title="↩️  Added to Queue",
                                  description=f"{title}"
                                  ).set_thumbnail(url=cover).set_footer(text=f"by {artist}")

            await interaction.edit_original_response(embed=embed)
