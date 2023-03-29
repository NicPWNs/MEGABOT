#!/usr/bin/env python3
import time
import discord
import random
import megacoin


async def double(ctx, confirm):

    if not confirm:
        embed = discord.Embed(color=0xf6be3c, title="⚖️  Double or Nothing",
                              description="Please confirm you want to play.")
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(color=0xf6be3c, title="⚖️  Double or Nothing",
                          description="<a:MEGACOINDOUBLE:1090716254203031632>").set_thumbnail(url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/double.gif")
    interaction = await ctx.respond(embed=embed)

    balance = await megacoin.balance(ctx.user)

    win = random.choice([0, 1])

    if win:
        description = "<:MEGACOINWIN:1090713259771953172>  You Win!"
        url = "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/win.gif"
        await megacoin.add(ctx.user, balance)
    else:
        description = "<:MEGACOINLOSE:1090713256865316914>  You Lose!"
        url = "https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/lose.gif"
        await megacoin.subtract(ctx.user, balance)

    time.sleep(random.randint(2, 10))

    embed = discord.Embed(
        color=0xf6be3c, title="⚖️  Double or Nothing", description=description).set_thumbnail(url=url)

    await interaction.edit_original_response(embed=embed)
