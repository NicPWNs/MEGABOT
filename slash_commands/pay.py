#!/usr/bin/env python3
import megacoin
import discord


async def pay(ctx, user, amount):

    balance = await megacoin.balance(ctx.user)

    description = "Sending..."
    embed = discord.Embed(
        color=0xa7d38a, title="💸  Payment", description=description)
    interaction = await ctx.respond(embed=embed)

    if amount < 0:
        description = "🤡  Nice try."
    elif balance == 0:
        description = "You have 0 <:MEGACOIN:1090620048621707324>"
    elif balance < amount:
        description = f"You don't have {str(amount)} <:MEGACOIN:1090620048621707324>"
    else:
        description = f"<@{ctx.user.id}> sent {str(amount)} <:MEGACOIN:1090620048621707324> to <@{str(user.id)}>"
        await megacoin.subtract(ctx.user, amount)
        await megacoin.add(user, amount)

    embed = discord.Embed(
        color=0xa7d38a, title="💸  Payment", description=description)
    await interaction.edit_original_response(embed=embed)
