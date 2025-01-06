#!/usr/bin/env python3
import typing
import discord
import wavelink


async def autoplay(ctx):
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

    # Disable autoplay
    if voice.autoplay == wavelink.AutoPlayMode.enabled:
        voice.autoplay = wavelink.AutoPlayMode.disabled
        embed = discord.Embed(color=0x5DACED, title="♾️  AutoPlay Disabled")

    # Enable autoplay
    elif voice.autoplay == wavelink.AutoPlayMode.disabled:
        voice.autoplay = wavelink.AutoPlayMode.enabled
        embed = discord.Embed(color=0x5DACED, title="♾️  AutoPlay Enabled")

    # Response
    await interaction.edit_original_response(embed=embed)
