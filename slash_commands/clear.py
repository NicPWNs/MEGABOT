#!/usr/bin/env python3
import os
import sys
import discord


async def clear(ctx):

    guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
    role = discord.utils.get(guild.roles, name="MEGAKILLERS")

    if role in ctx.user.roles:

        embed = discord.Embed(
            color=0xdd2f45, title="🧹  Cleared MEGATEST Commands!")
        await ctx.respond(embed=embed)

        bot = discord.Bot(intents=discord.Intents.all())
        await bot.start(os.getenv('DISCORD_TEST_TOKEN'))
        await bot.sync_commands(commands=[])
        await bot.close()

    else:
        embed = discord.Embed(color=0xdd2f45, title="❌ Permission Denied")
        await ctx.respond(embed=embed)
