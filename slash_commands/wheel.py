#!/usr/bin/env python3
import time
import discord
import random
import megacoin


async def wheel(ctx, wager):

    balance = await megacoin.balance(ctx.user)

    if balance == 0:
        embed = discord.Embed(
            color=0x9366cd, title="☸️  Spin the Wheel", description=f"You have 0 <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return
    elif balance < wager:
        embed = discord.Embed(
            color=0x9366cd, title="☸️  Spin the Wheel", description=f"You don't have {str(wager)} <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(color=0x9366cd, title="☸️  Spin the Wheel", description="Spinning...").set_thumbnail(
        url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/wheel.png")
    interaction = await ctx.respond(embed=embed)

    spin = random.choice([0, 0.5, 0.5, 1, 1, 3, 3, 5])
    win = wager * spin

    description = f"<@{ctx.user.id}> won {str(win)} <:MEGACOIN:1090620048621707324> with a wager of {str(wager)} <:MEGACOIN:1090620048621707324>!"
    url = "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/wheel.png"

    await megacoin.subtract(ctx.user, wager)
    await megacoin.add(ctx.user, win)

    embed = discord.Embed(
        color=0x9366cd, title="☸️  Spin the Wheel", description=description).set_thumbnail(url=url).set_footer(text=f"Their balance is now {await megacoin.balance(ctx.user)}")

    await interaction.edit_original_response(embed=embed)
