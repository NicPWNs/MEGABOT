#!/usr/bin/env python3
import discord


async def bless(ctx):

    embed = discord.Embed(color=0xffac33, title="✨  The mess has been blessed!")

    await ctx.respond(embed=embed)
