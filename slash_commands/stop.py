#!/usr/bin/env python3
import discord


async def stop(ctx, queued):

    embed = discord.Embed(color=0xfee9b6,
                          title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    try:
        await voice.disconnect()
        queued.clear()
        embed = discord.Embed(color=0xdd2f45, title="🔇  Music Stopped")

    except:
        embed = discord.Embed(color=0xdd2f45, title="❌  MEGABOT Is Not In Voice").set_thumbnail(
            url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif")
        pass

    await interaction.edit_original_response(embed=embed)
