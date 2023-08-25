#!/usr/bin/env python3
import modules.megacoin as megacoin


async def balance(ctx, user):

    if not user:
        await ctx.respond(content=f"<@{ctx.user.id}>'s balance is **{await megacoin.balance(ctx.user)}** <:MEGACOIN:1090620048621707324>")
    else:
        await ctx.respond(content=f"<@{user.id}>'s balance is **{await megacoin.balance(user)}** <:MEGACOIN:1090620048621707324>")
