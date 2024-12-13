#!/usr/bin/env python3
import re
import typing
import discord
import wavelink


async def skip(ctx):
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

    # Turn replay off
    if voice.queue.mode == wavelink.QueueMode.loop:
        voice.queue.mode = wavelink.QueueMode.normal

    # Skip song
    await voice.skip()

    # Autoplay starts
    if voice.current == None:
        embed = discord.Embed(
            color=0x5DACED,
            title="♾️  AutoPlay Running",
        )

    # Next song
    else:
        # Clean song title
        title = re.sub(r"\s*[\(\[][^)]*[\)\]]", "", voice.current.title).strip()

        embed = (
            discord.Embed(
                color=0x5DACED,
                title="🎵  Now Playing",
                description=f"[**{title}**]({voice.current.uri})",
            )
            .set_thumbnail(url=voice.current.artwork)
            .set_footer(text=f"by {voice.current.author}")
        )

    # Response
    await interaction.edit_original_response(embed=embed)
