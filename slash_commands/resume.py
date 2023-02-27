#!/usr/bin/env python3
import discord


async def resume(ctx):

    await ctx.respond(content="*⏳ Loading...*")

    voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    try:
        if voice.is_paused():
            voice.resume()

            content = f"**▶️  Music Resumed!**"

        else:
            content = f"**❌  Music Is Not Paused!**"
    except:
        content = f"**❌  MEGABOT is not connected!**"
        pass

    await ctx.edit(content=content)
