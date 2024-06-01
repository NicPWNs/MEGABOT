#!/usr/bin/env python3
import time
import discord
import random
import modules.megacoin as megacoin


async def wheel(ctx, wager):

    balance = await megacoin.balance(ctx.user)

    if wager < 0:
        embed = discord.Embed(
            color=0x9366CD, title="☸️  Spin the Wheel", description="🤡  Nice try."
        )
        await ctx.respond(embed=embed)
        return
    elif balance == 0:
        embed = discord.Embed(
            color=0x9366CD,
            title="☸️  Spin the Wheel",
            description="You have 0 <:MEGACOIN:1090620048621707324>",
        )
        await ctx.respond(embed=embed)
        return
    elif balance < wager:
        embed = discord.Embed(
            color=0x9366CD,
            title="☸️  Spin the Wheel",
            description=f"You don't have {str(wager)} <:MEGACOIN:1090620048621707324>",
        )
        await ctx.respond(embed=embed)
        return

    spin = random.choice([0, 0.5, 0.5, 1, 1, 1.5, 1.5, 2])
    diff = random.choice([1, 2])
    win = int(wager * spin)

    url = f"https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/{str(spin)}-{str(diff)}.gif"
    embed = discord.Embed(
        color=0x9366CD, title="☸️  Spin the Wheel", description="Spinning..."
    ).set_thumbnail(url=url)
    interaction = await ctx.respond(embed=embed)

    time.sleep(5)
    await megacoin.subtract(ctx.user, wager)
    await megacoin.add(ctx.user, win)

    description = f"<@{ctx.user.id}> wagered {str(wager)} <:MEGACOIN:1090620048621707324> and **won {str(win)}** <:MEGACOIN:1090620048621707324>!"
    url = f"https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/{str(spin)}-{str(diff)}.jpg"
    embed = (
        discord.Embed(
            color=0x9366CD, title="☸️  Spin the Wheel", description=description
        )
        .set_thumbnail(url=url)
        .set_footer(text=f"Their balance is now {await megacoin.balance(ctx.user)}")
    )

    await interaction.edit_original_response(embed=embed)
