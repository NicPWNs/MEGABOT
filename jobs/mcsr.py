#!/usr/bin/env python3
import discord
import requests
from datetime import datetime
import time


async def mcsr(bot):
    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="bot-testing")

    # Get current leaderboard data
    discord_ids = [member.id for member in guild.members]
    times = {}

    # Build leaderboard like in mc.py
    for discord_id in discord_ids:
        r = requests.get(
            f"https://mcsrranked.com/api/users/discord.{discord_id}"
        ).json()
        if r["status"] == "success":
            ranked_time = r["data"]["statistics"]["total"]["bestTime"]["ranked"]
            casual_time = r["data"]["statistics"]["total"]["bestTime"]["casual"]

            best_time = None
            if ranked_time is not None and casual_time is not None:
                best_time = min(int(ranked_time), int(casual_time))
            elif ranked_time is not None:
                best_time = int(ranked_time)
            elif casual_time is not None:
                best_time = int(casual_time)

            if best_time is not None:
                times[discord_id] = best_time

    # Find current #1 player
    if times:
        first_place_id = min(times.items(), key=lambda x: x[1])[0]

        # Get MEGARUNNER role
        megarunner_role = discord.utils.get(guild.roles, name="MEGARUNNER")

        if megarunner_role:
            # Remove role from all members who have it
            for member in megarunner_role.members:
                await member.remove_roles(megarunner_role)

            # Add role to new #1
            first_place_member = guild.get_member(first_place_id)
            if first_place_member:
                await first_place_member.add_roles(megarunner_role)

    # Continue with existing speedrun check code
    current_time = time.time()
    ten_mins_ago = current_time - (10 * 60)

    for discord_id in discord_ids:
        matches = requests.get(
            f"https://mcsrranked.com/api/users/discord.{discord_id}/matches"
        ).json()

        if matches["status"] == "success":
            for match in matches["data"]:
                match_time = match["date"]

                if match_time >= ten_mins_ago:
                    # Convert milliseconds to min:sec format
                    run_time_ms = match["result"]["time"]
                    minutes = run_time_ms // 60000
                    seconds = (run_time_ms % 60000) // 1000

                    # Get list of all players in the match
                    players = [p["nickname"] for p in match["players"]]
                    versus_text = " **vs** ".join(players)

                    # Format date
                    date_str = datetime.fromtimestamp(match_time).strftime(
                        "%Y-%m-%d %H:%M"
                    )

                    # Create and send individual embed for each run
                    description = (
                        f"<@{discord_id}> ({players[0]})  -  **{minutes}:{seconds:02d}**\n\n"
                        f"__Match:__ {versus_text}"
                    )

                    embed = discord.Embed(
                        color=0x86CE34,
                        title="<:MCSR:1372588978959548527>  New Minecraft Speed Run!",
                        description=description,
                    ).set_footer(text=date_str)
                    await channel.send(embed=embed)
