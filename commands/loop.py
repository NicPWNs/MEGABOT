#!/usr/bin/env python3
import typing
import discord
import wavelink


async def loop(ctx):
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

    # Turn loop off
    if voice.queue.mode == wavelink.QueueMode.loop_all:
        voice.queue.mode = wavelink.QueueMode.normal

        embed = discord.Embed(
            color=0x5DACED,
            title="🔁  Loop Turned Off  ❌",
        )

    # Turn loop on
    else:
        voice.queue.mode = wavelink.QueueMode.loop_all

        embed = discord.Embed(
            color=0x5DACED,
            title="🔁  Looping Queue",
        )

    # Response
    await interaction.edit_original_response(embed=embed)
