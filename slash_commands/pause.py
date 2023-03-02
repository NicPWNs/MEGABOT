#!/usr/bin/env python3
import discord


async def pause(ctx):

    embed = discord.Embed(color=0xfee9b6,
                        title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    try:
        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(color=0x3a88c2, title="▶️  Music Resumed")

        else:
            voice.pause()
            embed = discord.Embed(color=0x3a88c2, title="⏸️  Music Paused")

    except:
        embed = discord.Embed(color=0xdd2f45, title="❌  MEGABOT Is Not In Voice")
        pass

    await interaction.edit_original_response(embed=embed)
