#!/usr/bin/env python3
import os
import openai


async def image(ctx, prompt):

    openai.api_key = str(os.getenv('OPENAI_TOKEN'))

    await ctx.respond(content='*⏳ Loading...*')

    r = openai.Image.create(prompt=prompt, n=1, size="1024x1024", user=str(ctx.user.id))

    image = r.data[0].url

    await ctx.edit(content=image)
