#!/usr/bin/env python3
import os
import discord
from github import Github


async def bug(ctx, title, description):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    G = Github(os.getenv("GITHUB_TOKEN"))
    repo = G.get_repo("NicPWNs/MEGABOT")
    label = repo.get_label("bug")
    submitter = ctx.user.display_name
    description = description + f"\n\n> Submitted by `{submitter}`"
    issue = repo.create_issue(
        title=title, body=description, labels=[label], assignee="NicPWNs"
    )

    embed = discord.Embed(
        color=0x69A24A,
        title=f"🪲  Created New Bug #{issue.number}",
        description=f"[{issue.title}](https://github.com/NicPWNs/MEGABOT/issues/{issue.number})",
    )

    await interaction.edit_original_response(embed=embed)
