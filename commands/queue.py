#!/usr/bin/env python3
import discord
import os


async def queue(ctx, queued):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if not voice:
        embed = discord.Embed(color=0xdd2f45, title="❌  MEGABOT Is Not In Voice").set_thumbnail(
            url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif")
        await interaction.edit_original_response(embed=embed)

    else:
        description = ""
        num = 1

        if len(queued) == 0:
            description = "Queue is empty!"

        else:
            for song in queued:
                description += f"{num}. {os.path.splitext(song)[0]}\n"
                num += 1

        embed = discord.Embed(
            color=0x5daced, title="🔢  Current Queue", description=description)
        await interaction.edit_original_response(embed=embed)
