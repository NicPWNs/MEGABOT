#!/usr/bin/env python3
import os
import requests


async def cs(ctx, username):

    await ctx.respond(content="*⏳ Loading...*")

    headers = {
        "TRN-Api-Key": os.getenv('TRN_KEY'),
    }

    r = requests.get(
        'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/' + username, headers=headers).json()

    handle = r["data"]["platformInfo"]["platformUserHandle"]

    types = [
        "timePlayed",
        "score",
        "kills",
        "deaths",
        "kd",
        "damage",
        "headshots",
        "shotsFired",
        "shotsHit",
        "shotsAccuracy",
        "snipersKilled",
        "bombsPlanted",
        "bombsDefused",
        "moneyEarned",
        "hostagesRescued",
        "mvp",
        "wins",
        "ties",
        "matchesPlayed",
        "losses",
        "roundsPlayed",
        "roundsWon",
        "wlPercentage",
        "headshotPct",
    ]

    stat = f"__**{handle} CS2 Stats:**__\n"

    for i in range(0, len(types)):
        stat += "**" + \
            str(r["data"]["segments"][0]["stats"]
                [types[i]]["displayName"]) + ":**  " + \
            str(r["data"]["segments"][0]["stats"]
                [types[i]]["displayValue"]) + "\n"

    await ctx.edit(content=f"{stat}")
