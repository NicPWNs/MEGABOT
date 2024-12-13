#!/usr/bin/env python3
import typing
import discord
import wavelink


async def pause(ctx):
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

    # Pause
    if not voice.paused:
        await voice.pause(True)
        embed = discord.Embed(color=0x5DACED, title="⏸️  Music Paused")

    # Resume
    elif voice.paused:
        await voice.pause(False)
        embed = discord.Embed(color=0x5DACED, title="▶️  Music Resumed")

    # Not playing
    else:
        embed = discord.Embed(color=0x5DACED, title="⏯️  No Music Playing!")

    # Send response
    await interaction.edit_original_response(embed=embed)
