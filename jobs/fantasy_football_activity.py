#!/usr/bin/env python3
import os
import time
import discord
import convertapi
from datetime import datetime
from espn_api.football import League


async def fantasy_football_activity(bot):

    # Need this API to convert SVG images
    convertapi.api_secret = os.getenv("CONVERT_API")

    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="bot-testing")

    # Get the current NFL season year
    if int(datetime.now().month) < 4:
        year = int(datetime.now().year) - 1
    else:
        year = int(datetime.now().year)

    # Find the league
    league = League(
        swid=os.getenv("ESPN_SWID"),
        espn_s2=os.getenv("ESPN_S2"),
        league_id=192814871,
        year=year,
    )

    # Get the last 25 activities assuming more than 25 didn't happen in the last 24 hours
    activities = league.recent_activity(size=25)

    # If no activities
    if activities == []:
        return

    # If the latest activity didn't happen in the last 24 hours then don't run
    if activities[0].date < int(time.time() * 1000) - 24 * 60 * 60 * 1000:
        return

    # Reverse the activities so they are chronologically descending
    activities.reverse()

    # Description will hold a concatenated string of all actions within an activity
    description = ""

    embed = discord.Embed(
        color=0xFFFFFF,
        title="🏈 Fantasy Football",
        description="Last 24 Hours of Activity",
    ).set_thumbnail(
        url="https://espnpressroom.com/us/files/2016/08/Fantasy-Football-App-LOGO.png"
    )
    await channel.send(embed=embed)

    for activity in activities:
        # Only post activities that happened in the last 24 hours
        if activity.date < int(time.time() * 1000) - 24 * 60 * 60 * 1000:
            continue
        logo_url = activity.actions[0][0].logo_url
        # Convert native SVG logos to PNGs so Discord can use them
        if "svg" in activity.actions[0][0].logo_url:
            logo_url = convertapi.convert(
                "png", {"File": activity.actions[0][0].logo_url}, from_format="svg"
            ).file.url
        for action in activity.actions:
            description += f"**{action[1]}**  {action[2].name}" + "\n"
        if "DROPPED" in description and "ADDED" in description:
            color = 0x5EAEEB
        elif "DROPPED" in description:
            color = 0xE52534
        elif "ADDED" in description:
            color = 0x34E718
        embed = discord.Embed(
            color=color,
            title=f"{activity.actions[0][0].team_name}",
            description=description,
        ).set_thumbnail(url=logo_url)
        await channel.send(embed=embed)
        description = ""
