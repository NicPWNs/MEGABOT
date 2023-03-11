#!/usr/bin/env python3
import discord


async def bless(ctx):

    embed = discord.Embed(color=0xffac33, title="✨  The mess has been blessed!").set_thumbnail(url="https://user-images.githubusercontent.com/23003787/222802744-34fa733e-32d2-4093-be09-7a9d433f9df2.gif")

    await ctx.respond(embed=embed)
