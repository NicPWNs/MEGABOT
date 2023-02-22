async def math(ctx, expression):

    response = str(eval(expression))

    await ctx.respond(content=f"{response}")
