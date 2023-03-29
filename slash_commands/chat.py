#!/usr/bin/env python3
import os
import openai


async def chat(ctx, prompt):

    await ctx.respond(content='*⏳ Loading...*')

    openai.api_key = os.getenv('OPENAI_TOKEN')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f'❌ **ERROR: Your prompt is innapropriate.**')
        return

    stream = []
    try:
        for r in openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                              messages=[{"role": "system", "content": "You are a relaxed, sarcastic, and funny bot friend, named MEGABOT that serves the MEGACORD Discord server. Administrators are called MEGALORDS, moderators are called MEGAMODS, and everyone else is MEGAENJOYERS. The currency of the server is called MEGACOINS. Make sure to reference that you are a government goon in some responses."},
                                                        {"role": "assistant", "content": f"{ctx.user.display_name} is talking to you. Nic (NicPWNs) is an elite hacker. Randy codes in Java too much. Alican (wildman) is Turkish. Joey (tiny bro) doesn't have enough clearance. Brendan (Sundrop) loves drama. Damien is bad at video games. Josh (Blend) is stuck in the Navy."},
                                                        {'role': 'user', 'content': prompt}],
                                              user=str(ctx.user.id),
                                              stream=True):
            try:
                stream.append(r.choices[0].delta.content)
                result = "".join(stream).strip()
                await ctx.edit(content=f'{result}')
            except:
                pass
    except:
        await ctx.edit(content=f'❌ **ERROR: GPT is currently overloaded. Please try again.**')
        return
