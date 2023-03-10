#!/usr/bin/env python3
import os
import openai


async def image(ctx, prompt):

    await ctx.respond(content='*⏳ Loading...*')

    openai.api_key = os.getenv('OPENAI_TOKEN')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f'❌ **ERROR: Your prompt is innapropriate.**')
        return

    #try:
    r = openai.Image.create(prompt=prompt, n=1, size="1024x1024", response_format="b64_json", user=str(ctx.user.id))

    image = "data:image/png;base64," + r.data[0].b64_json

    content = image #+ f"\n ❝ {prompt} ❞"

    await ctx.edit(content=content)
    #except:
    await ctx.edit(content=f'❌ **ERROR: Your prompt may contain safety issues. Please try a different prompt.**')
