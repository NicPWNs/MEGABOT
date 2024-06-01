#!/usr/bin/env python3
import discord
from random import random


async def coin(ctx):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")

    interaction = await ctx.respond(embed=embed)

    coin = "🗣️   Heads!"

    if random() < 0.5:
        coin = "☄️   Tails!"

    embed = discord.Embed(color=0xF6BE3C, title="🪙   Coin Flip", description=coin)

    await interaction.edit_original_response(embed=embed)
