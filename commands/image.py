#!/usr/bin/env python3
import string
import discord
from openai import OpenAI


async def image(ctx, prompt):

    embed = discord.Embed(
        color=0xFEE9B6,
        title="⏳  Generating Image...",
        description=f'**Prompt:** "{prompt}"',
    )

    interaction = await ctx.respond(embed=embed)

    openai = OpenAI()

    moderation = openai.moderations.create(input=prompt)

    if moderation.results[0].flagged:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌  Error",
            description=f"Your prompt is innapropriate.",
        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    try:
        r = openai.images.generate(
            prompt=prompt, n=1, size="1024x1024", user=str(ctx.user.id)
        )

        url = r.data[0].url

        embed = discord.Embed(
            color=0x5965F3,
            title=f'🖼️  " {string.capwords(prompt)} "',
            description=f"by <@{ctx.user.id}>",
        ).set_image(url=url)

        await interaction.edit_original_response(embed=embed)

    except:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌  Error",
            description=f"Your prompt may contain safety issues. Please try a different prompt.",
        ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
