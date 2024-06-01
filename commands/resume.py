#!/usr/bin/env python3
import discord


async def resume(ctx):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    try:
        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(color=0x5DACED, title="▶️  Music Resumed")
        elif voice.is_playing():
            embed = discord.Embed(color=0x5DACED, title="▶️  Music Already Playing!")
        else:
            embed = discord.Embed(color=0x5DACED, title="⏯️  No Music Playing!")

    except:
        embed = discord.Embed(
            color=0xDD2F45, title="❌  MEGABOT Is Not In Voice"
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif"
        )
        pass

    await interaction.edit_original_response(embed=embed)
