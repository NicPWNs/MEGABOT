#!/usr/bin/env python3
import os
import requests


async def nasa(ctx, details):
    r = requests.get(
        "https://api.nasa.gov/planetary/apod?api_key=" + str(os.getenv("NASA_KEY"))
    ).json()

    desc = ""

    if details:
        desc = r["explanation"]

    response = r["url"] + "\n" + desc

    await ctx.respond(content=f"{response}")
