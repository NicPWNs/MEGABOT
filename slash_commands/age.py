#!/usr/bin/env python3
import discord
import requests


async def age(ctx, name):
    r = requests.get('https://api.agify.io/?name=' + name).json()
    age = r["age"]

    if age is None:
        response = "Name not found!"
    else:
        response = f"I guess the age of \"{name}\" is {age}!"

    embed = discord.Embed(color=0xffac33, title="🔢  Age Guesser", description=response)

    await ctx.respond(embed=embed)
