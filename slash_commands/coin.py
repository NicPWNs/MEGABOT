#!/usr/bin/env python3
import discord
from random import random

async def coin(ctx):

    embed = discord.Embed(color=0xfee9b6,
                        title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    coin = "🗣️   Heads!"

    if random() < .5:
        coin = "☄️   Tails!"

    embed = discord.Embed(color=0xf6be3c,
                          title="🪙   Coin Flip",
                          description=coin)

    await interaction.edit_original_response(embed=embed)
