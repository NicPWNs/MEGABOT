#!/usr/bin/env python3
import discord


async def math(ctx, expression):

    try:
        response = str(eval(expression))
    except:
        response = "Invalid Expression!"

    embed = discord.Embed(color=0x5b8f3c, title="🧮  Math",
                          description=response)

    await ctx.respond(embed=embed)
