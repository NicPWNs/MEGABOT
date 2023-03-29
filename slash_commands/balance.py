#!/usr/bin/env python3
import megacoin


async def balance(ctx):

    await ctx.respond(content=f"<@{ctx.user.id}>'s balance is **{await megacoin.balance(ctx.user)}** <:MEGACOIN:1090620048621707324>")
