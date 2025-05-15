#!/usr/bin/env python3
import discord
import requests


async def mc(ctx):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    discord_ids = [member.id for member in ctx.guild.members]
    description = ""
    times = {}

    for discord_id in discord_ids:
        r = requests.get(
            f"https://mcsrranked.com/api/users/discord.{discord_id}"
        ).json()
        if r["status"] == "error":
            continue
        elif r["status"] == "success":
            ranked_time = r["data"]["statistics"]["total"]["bestTime"]["ranked"]
            casual_time = r["data"]["statistics"]["total"]["bestTime"]["casual"]

            # Initialize best_time as None
            best_time = None

            # Check if either time is not null
            if ranked_time is not None and casual_time is not None:
                best_time = min(int(ranked_time), int(casual_time))
            elif ranked_time is not None:
                best_time = int(ranked_time)
            elif casual_time is not None:
                best_time = int(casual_time)

            # Only add to times dictionary if there's a valid time
            if best_time is not None:
                times[r["data"]["nickname"]] = (best_time, discord_id)

    number = 0

    # Sort times dictionary by values (best times) in ascending order
    sorted_times = dict(sorted(times.items(), key=lambda x: x[1][0]))

    for nickname, (best_time, discord_id) in sorted_times.items():
        # Convert milliseconds to minutes and seconds
        minutes = best_time // 60000
        seconds = (best_time % 60000) // 1000
        time_str = f"{minutes}:{seconds:02d}"
        description += f"{number + 1}. <@{discord_id}> ({nickname}) - **{time_str}**\n"
        number += 1

    if description == "":
        description = "No one in MEGACORD has completed a speed run!"

    embed = discord.Embed(
        color=0x86CE34,
        title="<:MCSR:1372588978959548527>  Minecraft Speed Running Leaderboard",
        description=description,
    )
    await interaction.edit_original_response(embed=embed)

    return
