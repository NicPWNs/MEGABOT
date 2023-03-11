#!/usr/bin/env python3
import discord
import requests


async def age(ctx, name):
    r = requests.get('https://api.agify.io/?name=' + name).json()
    age = r["age"]

    name = str.title(name)

    if age is None:
        response = f"Name \"{name}\" not found!"
    else:
        response = f"I guess the age of \"{name}\" is **{age}**!"

    embed = discord.Embed(color=0x3a88c2, title="🔢  Age Guess", description=response)

    await ctx.respond(embed=embed)
