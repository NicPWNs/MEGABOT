#!/usr/bin/env python3
import os
import discord
from github import Github


async def version(ctx):

    G = Github(os.getenv("GITHUB_TOKEN"))
    repo = G.get_repo("NicPWNs/MEGABOT")
    release = repo.get_releases()[0].title

    embed = discord.Embed(
        color=0xD89B82,
        title="📦 Current Version",
        description=f"The latest <@{ctx.bot.user.id}> release is [**{release}**](https://github.com/NicPWNs/MEGABOT/releases)",
    )

    await ctx.respond(embed=embed)
