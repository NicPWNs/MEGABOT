#!/usr/bin/env python3
import os
import discord
from github import Github


async def start(ctx):

    guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
    role = discord.utils.get(guild.roles, name="MEGAKILLERS")

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    if role in ctx.user.roles:

        G = Github(os.getenv("GITHUB_TOKEN"))
        repo = G.get_repo("NicPWNs/MEGABOT")
        workflow = repo.get_workflow("Push-to-EC2")
        workflow.create_dispatch(ref=repo.get_branch("main"))

        embed = discord.Embed(
            color=0x69A24A,
            title=f"🟢  Restarting...",
            description=f"<@{ctx.bot.user.id}> should be back online shortly!",
        )

        await interaction.edit_original_response(embed=embed)

    else:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌ Permission Denied",
            description=f"Nice try <@{ctx.user.id}>!",
        )
        await interaction.edit_original_response(embed=embed)
