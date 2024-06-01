#!/usr/bin/env python3
import os
import openai


async def code(ctx, prompt):

    await ctx.respond(content="*⏳ Loading...*")

    openai.api_key = os.getenv("OPENAI_TOKEN")

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f"❌ **ERROR: Your prompt is innapropriate.**")
        return

    stream = []
    try:
        for r in openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful Discord coding bot named MEGABOT that generates code from OpenAI's GPT model. Default to Python if another language is not specified. Limit additional context and dialogue, just focus on providing code. Use markdown with syntax highlighting.",
                },
                {"role": "user", "content": prompt},
            ],
            user=str(ctx.user.id),
            stream=True,
        ):
            try:
                stream.append(r.choices[0].delta.content)
                result = "".join(stream).strip()
                await ctx.edit(content=result)
            except:
                pass

    except:
        await ctx.edit(
            content=f"❌ **ERROR: GPT is currently overloaded. Please try again.**"
        )
        return
