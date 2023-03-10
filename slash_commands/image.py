#!/usr/bin/env python3
import os
import openai


async def image(ctx, prompt):

    openai.api_key = os.getenv('OPENAI_TOKEN')

    await ctx.respond(content='*⏳ Loading...*')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f'❌ **ERROR: Your prompt is innapropriate.**')
        return

    try:
        r = openai.Image.create(prompt=prompt, n=1, size="1024x1024", user=str(ctx.user.id))

        image = r.data[0].url

        content = image + f"\n ❝ {prompt} ❞"

        await ctx.edit(content=content)
    except:
        await ctx.edit(content=f'❌ **ERROR: Your prompt may contain safety issues. Please try a different prompt.**')
