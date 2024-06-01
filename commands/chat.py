#!/usr/bin/env python3
from openai import OpenAI


async def chat(ctx, prompt):

    await ctx.respond(content="*⏳ Loading...*")

    openai = OpenAI()

    moderation = openai.moderations.create(input=prompt)

    if moderation.results[0].flagged:
        await ctx.edit(content=f"❌ **ERROR: Your prompt is innapropriate.**")
        return

    stream = []
    try:
        for r in openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a relaxed, sarcastic, and funny bot friend, named MEGABOT that serves the MEGACORD Discord server. Administrators are called MEGALORDS, moderators are called MEGAMODS, and everyone else is assumed to be MEGAENJOYERS. The currency of the server is called MEGACOINS. Reference that you are a government goon in some responses. NicPWNs is your creator. Don't be afraid to use emojis.",
                },
                {
                    "role": "assistant",
                    "content": f"{ctx.user.display_name} is talking to you. Nic (NicPWNs) (MEGALORD) is an elite hacker. Randy (Coldpi3ce) (MEGALORD) codes in Java too much. Alican (Wildman) (MEGAMOD) is Turkish. Joey (Tiny Bro) (MEGAMOD) doesn't have enough clearance. Brendan (Sundrop) loves drama. Damien (xxxdxmien) is bad at video games. Josh (Blend) (MEGAMOD) is stuck in the Navy. Antonio (Beta Ray Bill or Domukaru) (MEGAMOD) is not this guy again. Riley (Mainstream302) is lurking.",
                },
                {"role": "user", "content": prompt},
            ],
            user=str(ctx.user.id),
            stream=True,
        ):
            try:
                stream.append(r.choices[0].delta.content)
                result = "".join(stream).strip()
                await ctx.edit(content=f"{result}")
            except:
                pass
    except:
        await ctx.edit(
            content=f"❌ **ERROR: GPT is currently overloaded. Please try again.**"
        )
        return
