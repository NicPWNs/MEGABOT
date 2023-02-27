#!/usr/bin/env python3
import discord


async def stop(ctx):

    await ctx.respond(content="*⏳ Loading...*")

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()

    content = f"**🔇  Music Stopped!**"

    await ctx.edit(content=content)
