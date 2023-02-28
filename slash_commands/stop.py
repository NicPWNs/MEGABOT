#!/usr/bin/env python3
import discord


async def stop(ctx):

    await ctx.respond(content="*⏳ Loading...*")

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    try:
        await voice.disconnect()

        content = f"**🔇  Music Stopped!**"

    except:
        content = f"**❌  MEGABOT is not connected!**"
        pass

    await ctx.edit(content=content)
