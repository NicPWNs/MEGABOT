#!/usr/bin/env python3
import os
import time
import discord
import datetime
import convertapi
from espn_api.football import League

async def ffl(ctx):

    await ctx.respond(content="*⏳ Loading...*")

    convertapi.api_secret = os.getenv("CONVERT_API")

    # Find the league
    league = League(swid=os.getenv("ESPN_SWID"), espn_s2=os.getenv("ESPN_S2"), league_id=2108883860, year=int(datetime.date.today().year))

    # Get the last 25 activities assuming more than 25 didn't happen in the last 24 hours
    activities = league.recent_activity(size=25)

    # If the latest activity didn't happen in the last 24 hours then don't run
    if activities[0].date < int(time.time() * 1000) - 24*60*60*1000:
        return

    # Reverse the activities so they are chronologically descending
    activities.reverse()

    # Description will hold a concatenated string of all actions within an activity
    description = ""

    embed = discord.Embed(
        color=0xffffff,
        title="🏈 Fantasy Football",
        description="Last 24 Hours of Activity").set_thumbnail(url="https://espnpressroom.com/us/files/2016/08/Fantasy-Football-App-LOGO.png")
    await ctx.edit(embed=embed)

    for activity in activities:
        # Only post activities that happened in the last 24 hours
        if activity.date < int(time.time() * 1000) - 24*60*60*1000:
            continue
        logo_url = activity.actions[0][0].logo_url
        # Convert native SVG logos to PNGs so Discord can use them
        if "svg" in activity.actions[0][0].logo_url:
            logo_url = convertapi.convert('png', {
                'File': activity.actions[0][0].logo_url
            }, from_format = 'svg').file.url
        for action in activity.actions:
            description += f"**{action[1]}**  {action[2].name}" + "\n"
        if "DROPPED" in description and "ADDED" in description:
            color = 0x5eaeeb
        elif "DROPPED" in description:
            color = 0xe52534
        elif "ADDED" in description:
            color = 0x34e718
        embed = discord.Embed(
            color=color,
            title=f"{activity.actions[0][0].team_name}",
            description=description).set_thumbnail(url=logo_url)
        await ctx.channel.send(embed=embed)
        description = ""
