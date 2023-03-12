#!/usr/bin/env python3
import os
import sys
import discord


async def kill(ctx):

    guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
    role = discord.utils.get(guild.roles, name="MEGAKILLERS")

    if role in ctx.user.roles:

        pid = os.getpid()

        embed = discord.Embed(color=0xdd2f45, title="🛑  Stopping MEGABOT", description=f"<@{ctx.bot.id}> killed on PID {pid} !")
        await ctx.respond(embed=embed)

        # sys.exit()

    else:
        embed = discord.Embed(color=0xdd2f45, title="❌ Permission Denied", description=f"Nice try <@{ctx.user.id}>!")
        await ctx.respond(embed=embed)
