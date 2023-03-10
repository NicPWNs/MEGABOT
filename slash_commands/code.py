#!/usr/bin/env python3
import os
import openai


async def code(ctx, prompt):

    await ctx.respond(content='*⏳ Loading...*')

    openai.api_key = os.getenv('OPENAI_TOKEN')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f'❌ **ERROR: Your prompt is innapropriate.**')
        return

    stream = []
    try:
        for r in openai.Completion.create(model="code-davinci-002", prompt=prompt, stream=True):
            stream.append(r.choices[0].text)
            result = "".join(stream).strip()
            await ctx.edit(content=result)

        result = "".join(stream).strip()
        content = "\'\'\'\n" + result + "\n\'\'\'"
        await ctx.edit(content=content)

    except:
        await ctx.edit(content=f'❌ **ERROR: GPT is currently overloaded. Please try again.**')
        return
