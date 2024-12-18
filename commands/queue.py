#!/usr/bin/env python3
import re
import typing
import discord
import wavelink


async def queue(ctx):
    # Initial response
    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    # Get player
    voice = typing.cast(wavelink.Player, ctx.voice_client)

    # Not in voice
    if not voice:
        embed = discord.Embed(
            color=0xDD2F45, title="❌  MEGABOT Is Not In Voice"
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif"
        )
        await interaction.edit_original_response(embed=embed)
        return

    # Prepare variables
    description = ""
    num = 1

    # Clean song title
    title = re.sub(r"\s*[\(\[][^)]*[\)\]]", "", voice.current.title).strip()

    # Now playing
    description += f"__Now Playing 🎶:__ **{title}** - *{voice.current.author}*\n\n"

    # Songs in regular queue
    for song in voice.queue:
        title = re.sub(r"\s*[\(\[][^)]*[\)\]]", "", song.title).strip()
        description += f"{num}. **{song.title}** - *{song.author}*\n"
        num += 1

    # Songs in auto queue
    for song in voice.auto_queue[:10]:
        title = re.sub(r"\s*[\(\[][^)]*[\)\]]", "", song.title).strip()
        description += f"{num}. **{title}** - *{song.author}*  ♾️\n"
        num += 1

    # Queue mode
    emoji = "🔢"
    if voice.queue.mode == wavelink.QueueMode.loop_all:
        emoji = "🔁"
    elif voice.queue.mode == wavelink.QueueMode.loop:
        emoji = "🔂"

    # Return queue
    embed = discord.Embed(
        color=0x5DACED, title=f"{emoji}  Current Queue", description=description
    ).set_footer(text="♾️ Indicates AutoPlay")
    await interaction.edit_original_response(embed=embed)
