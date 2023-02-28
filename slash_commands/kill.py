#!/usr/bin/env python3
import os
import sys
import discord


async def kill(ctx):

    guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
    role = discord.utils.get(guild.roles, name="MEGAKILLERS")

    if role in ctx.user.roles:

        pid = os.getpid()

        content = f"🛑 **Stopping MEGABOT on PID {pid} !**"
        await ctx.respond(content=content)

        sys.exit()

    else:
        content = f"❌ **Permission Denied.** Nice try <@{ctx.user.id}>!"
        await ctx.respond(content=content)
