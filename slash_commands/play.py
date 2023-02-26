#!/usr/bin/env python3
import youtube_dl


async def play(ctx):

    content = ctx.message

    await ctx.respond(content=content)
