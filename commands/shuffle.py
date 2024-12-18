#!/usr/bin/env python3
import typing
import discord
import wavelink


async def shuffle(ctx):
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

    # Queue empty
    if len(voice.queue) == 0:
        embed = discord.Embed(color=0xDD2F45, title="❌  Queue Is Empty")
        await interaction.edit_original_response(embed=embed)
        return

    # Shuffle queue
    voice.queue.shuffle()

    # Response
    embed = discord.Embed(color=0x5DACED, title="🔀  Queue Shuffled")
    await interaction.edit_original_response(embed=embed)
