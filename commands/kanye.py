#!/usr/bin/env python3
import requests


async def kanye(ctx):
    r = requests.get("https://api.kanye.rest/").json()

    quote = r["quote"]
    content = f"<a:kanyePls:1081048056058871808>  💬  ❝ {quote} ❞"

    await ctx.respond(content=content)
