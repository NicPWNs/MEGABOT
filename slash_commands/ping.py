#!/usr/bin/env python3
import discord


async def ping(ctx):

    embed = discord.Embed(color=0xdc2e45, title="🏓  Pong!").set_thumbnail(url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/thumbnail.gif")

    await ctx.respond(embed=embed)
