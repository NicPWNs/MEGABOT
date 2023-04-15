#!/usr/bin/env python3
import discord


async def ping(ctx):

    latency = int(ctx.bot.latency * 1000)

    embed = discord.Embed(
        color=0xdc2e45, title=f"🏓  Pong! Latency is {latency}ms")

    await ctx.respond(embed=embed)
