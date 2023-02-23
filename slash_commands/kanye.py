import requests


async def kanye(ctx):
    r = requests.get('https://api.kanye.rest/').json()

    quote = r["quote"]
    response = f"<:kanye:1078059327891439657>💬  ❝ {quote} ❞"

    await ctx.respond(content=f"{response}")
