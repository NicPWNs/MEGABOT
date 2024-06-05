#!/usr/bin/env python3
import os
from github import Github


async def version(ctx):

    G = Github(os.getenv("GITHUB_TOKEN"))
    repo = G.get_repo("NicPWNs/MEGABOT")
    release = repo.get_releases()[0].title
    # TODO: Add Link to Release
    await ctx.respond(
        content=f"📦  The latest <@{ctx.bot.user.id}> release is **{release}**"
    )
