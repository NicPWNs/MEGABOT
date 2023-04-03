#!/usr/bin/env python3
import os
import string
import openai
import discord


async def image(ctx, prompt):

    embed = discord.Embed(color=0xfee9b6,
                          title="⏳  Generating Image...",
                          description=f"**Prompt:** \"{prompt}\""
                          )

    interaction = await ctx.respond(embed=embed)

    openai.api_key = os.getenv('OPENAI_TOKEN')

    moderation = openai.Moderation.create(input=prompt)

    if moderation.results[0].flagged:
        embed = discord.Embed(color=0xdd2f45,
                              title="❌  Error",
                              description=f"Your prompt is innapropriate."
                              ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
        return

    try:
        r = openai.Image.create(
            prompt=prompt, n=1, size="1024x1024", user=str(ctx.user.id))

        url = r.data[0].url

        embed = discord.Embed(
            color=0x5965f3, title=f"🖼️  \" {string.capwords(prompt)} \"", description=f"by <@{ctx.user.id}>").set_image(url=url)

        await interaction.edit_original_response(embed=embed)

    except:
        embed = discord.Embed(color=0xdd2f45,
                              title="❌  Error",
                              description=f"Your prompt may contain safety issues. Please try a different prompt."
                              ).set_thumbnail(url=ctx.user.display_avatar)

        await interaction.edit_original_response(embed=embed)
