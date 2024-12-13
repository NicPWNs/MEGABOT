#!/usr/bin/env python3
import discord


async def stop(ctx):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    try:
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        await voice.disconnect()

        embed = discord.Embed(color=0xDD2F45, title="🔇  Music Stopped")
    except:
        embed = discord.Embed(
            color=0xDD2F45, title="❌  MEGABOT Is Not In Voice"
        ).set_thumbnail(
            url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif"
        )
        pass

    await interaction.edit_original_response(embed=embed)
