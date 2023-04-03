#!/usr/bin/env python3
import time
import discord
import random
import megacoin


async def double(ctx, wager):

    balance = await megacoin.balance(ctx.user)

    if wager < 0:
        embed = discord.Embed(
            color=0x9366cd, title="⚖️  Double or Nothing", description="🤡  Nice try.")
        await ctx.respond(embed=embed)
        return
    elif balance == 0:
        embed = discord.Embed(
            color=0x9366cd, title="⚖️  Double or Nothing", description="You have 0 <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return
    elif balance < wager:
        embed = discord.Embed(
            color=0x9366cd, title="⚖️  Double or Nothing", description=f"You don't have {str(wager)} <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(color=0xffad32, title="⚖️  Double or Nothing", description="Flipping...").set_thumbnail(
        url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/double.gif")
    interaction = await ctx.respond(embed=embed)

    win = random.choice([0, 1])

    if win:
        description = f"<@{ctx.user.id}> wagered {wager} <:MEGACOIN:1090620048621707324> and doubled it!"
        url = "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/win.png"
        await megacoin.add(ctx.user, wager)
    else:
        description = f"<@{ctx.user.id}> wagered {wager} <:MEGACOIN:1090620048621707324> and lost it!"
        url = "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/lose.png"
        await megacoin.subtract(ctx.user, wager)

    time.sleep(random.randint(3, 10))

    embed = discord.Embed(
        color=0xffad32, title="⚖️  Double or Nothing", description=description).set_thumbnail(url=url).set_footer(text=f"Their balance is now {await megacoin.balance(ctx.user)}")

    await interaction.edit_original_response(embed=embed)
