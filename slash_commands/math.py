#!/usr/bin/env python3


async def math(ctx, expression):

    response = str(eval(expression))

    await ctx.respond(content=f"{response}")
