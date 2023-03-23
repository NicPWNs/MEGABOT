#!/usr/bin/env python3
from random_unicode_emoji import random_emoji


async def randomemoji(ctx):

    await ctx.respond(content=random_emoji()[0])
