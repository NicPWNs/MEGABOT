#!/usr/bin/env python3
import discord


async def ping(ctx):

    embed = discord.Embed(color=0xdc2e45, title="🏓  Pong!")

    await ctx.respond(embed=embed)
