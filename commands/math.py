#!/usr/bin/env python3
import discord
import ast


async def math(ctx, expression):

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        result = "Not a valid Python expression!"
        embed = discord.Embed(color=0x5B8F3C, title="🧮  Math", description=result)
        await ctx.respond(embed=embed)

    if not all(
        isinstance(
            node,
            (
                ast.Expression,
                ast.UnaryOp,
                ast.unaryop,
                ast.BinOp,
                ast.operator,
                ast.Constant,
            ),
        )
        for node in ast.walk(tree)
    ):
        result = "Not a valid mathematical expression!"
        embed = discord.Embed(color=0x5B8F3C, title="🧮  Math", description=result)
        await ctx.respond(embed=embed)
    else:
        result = eval(compile(tree, filename="", mode="eval"))
        embed = discord.Embed(color=0x5B8F3C, title="🧮  Math", description=result)
        await ctx.respond(embed=embed)
