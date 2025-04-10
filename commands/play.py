#!/usr/bin/env python3
import re
import time
import typing
import discord
import wavelink


async def play(ctx, search):
    # Initial response
    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    # Get player
    voice = typing.cast(wavelink.Player, ctx.voice_client)

    # Join voice if not already
    if not voice:
        voice = await ctx.author.voice.channel.connect(cls=wavelink.Player)

    # Check if user is in voice with bot
    if ctx.author.voice.channel.id != voice.channel.id:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌  Error",
            description=f"<@{ctx.user.id}> is not in <#{voice.channel.id}> with <@1077260321833635941>!",
        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    # Check if the input is a URL but not a YouTube URL
    if search.startswith(("http://", "https://")) and not bool(
        re.match(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$", search)
    ):
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌  Error",
            description="Only YouTube is supported. Please provide a YouTube URL or a search term.",
        ).set_thumbnail(url=ctx.user.display_avatar)
        await interaction.edit_original_response(embed=embed)
        return

    # Search for songs
    songs = await wavelink.Playable.search(search)

    # Song not found
    if not songs:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌  Error",
            description=f"**No results found for:** {search}",
        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    # Rest of playlist
    playlist = []

    # Parse songs or playlist
    if type(songs) == wavelink.tracks.Playlist:
        playlist = songs[1:]

    song = songs[0]

    # Turn on autoplay
    voice.autoplay = wavelink.AutoPlayMode.enabled

    if voice.playing == True:

        # Add song to queue
        voice.queue.put(song)
        voice.queue.put(playlist)

        # Added to queue
        embed = (
            discord.Embed(
                color=0x5DACED,
                title="↩️  Added to Queue",
                description=f"[**{song.title}**]({song.uri})",
            )
            .set_thumbnail(url=song.artwork)
            .set_footer(text=f"by {song.author}")
        )

        # Response
        await interaction.edit_original_response(embed=embed)

    else:
        # Turn down volume before playing
        await voice.set_volume(15)

        # Play and populate autoqueue
        await voice.play(song, populate=True)

        # Add rest of playlist
        voice.queue.put(playlist)

        # Clean song title
        title = re.sub(r"\s*[\(\[][^)]*[\)\]]", "", song.title).strip()

        # Calculate progress bar
        position = int(voice.position / 1000)
        length = int(song.length / 1000)
        increment = int(length / 15)

        while position < length:
            position = voice.position / 1000
            bars = int(position / increment)
            status = ("▬" * bars) + "🔘" + ("▬" * (15 - bars))

            # Calculate current time and total time
            current_minutes = int(position // 60)
            current_seconds = int(position % 60)
            total_minutes = int(length // 60)
            total_seconds = int(length % 60)

            # Now playing
            embed = (
                discord.Embed(
                    color=0x5DACED,
                    title="🎵  Now Playing",
                    description=f"[**{title}**]({song.uri})\n\n▐{status}▌\n`[{current_minutes}:{current_seconds:02d}]`                      `[{total_minutes}:{total_seconds:02d}]`",
                )
                .set_thumbnail(url=song.artwork)
                .set_footer(text=f"by {song.author}")
            )

            # Response
            await interaction.edit_original_response(embed=embed)

            time.sleep(1)
