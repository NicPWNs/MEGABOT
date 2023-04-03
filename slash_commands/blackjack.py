#!/usr/bin/env python3
import time
import discord
import random
import megacoin


async def blackjack(ctx, wager):

    balance = await megacoin.balance(ctx.user)

    description = "Dealing..."
    embed = discord.Embed(
        color=0x9366cd, title="🃏  Blackjack", description=description)

    if balance == 0:
        description = f"You have 0 <:MEGACOIN:1090620048621707324>"
        await ctx.respond(embed=embed)
        return
    elif balance < wager:
        description = f"You don't have {str(wager)} <:MEGACOIN:1090620048621707324>"
        await ctx.respond(embed=embed)
        return

    face = random.choice(['2', '3', '4', '5', '6', '7',
                          '8', '9', '10', 'j', 'q', 'k', 'a'])
    suit = random.choice(['c', 'd', 'h', 's'])
    card = face + suit

    emojis = ctx.guild.emojis
    emoji = discord.utils.get(emojis, name=card)

    interaction = await ctx.respond(embed=embed)
    await ctx.channel.send("Dealer:")
    dealer = await ctx.channel.send("<:MEGACARD:1091828635138281482>" + str(emoji))

    await interaction.edit_original_response(embed=embed)
