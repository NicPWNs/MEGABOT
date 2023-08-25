#!/usr/bin/env python3
from random_unicode_emoji import random_emoji


async def random_unicode_emoji(ctx):

    await ctx.respond(content=random_emoji()[0])
