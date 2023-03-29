#!/usr/bin/env python3


async def math(ctx, expression):

    try:
        response = str(eval(expression))
    except:
        await ctx.respond(content="Invalid Expression!")
        return

    await ctx.respond(content=f"{response}")
