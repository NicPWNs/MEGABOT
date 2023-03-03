#!/usr/bin/env python3
import discord
from random import randint

async def dice(ctx):

    embed = discord.Embed(color=0xfee9b6,
                        title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    dice = randint(1,6)

    if dice == 1:
        roll = "You Rolled 1️⃣"
    if dice == 2:
        roll = "You Rolled 2️⃣"
    if dice == 3:
        roll = "You Rolled 3️⃣"
    if dice == 4:
        roll = "You Rolled 4️⃣"
    if dice == 5:
        roll = "You Rolled 5️⃣"
    if dice == 6:
        roll = "You Rolled 6️⃣" 

    embed = discord.Embed(color=0xea596e,
                          title="🎲   Dice Roll",
                          description=roll)

    await interaction.edit_original_response(embed=embed)
