#!/usr/bin/env python3
import os
import requests
import discord


async def stock(ctx, symbol):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    STOCK_KEY = str(os.getenv('STOCK_KEY'))

    r = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={STOCK_KEY}').json()

    symbol = r["Global Quote"]["01. symbol"]
    price = str(round(float(r["Global Quote"]["05. price"]), 2))
    change = str(round(float(r["Global Quote"]["09. change"]), 2))

    emoji = "📈"
    color = 0x77b354

    if "-" in change:
        emoji = "📉"
        color = 0xdd2f45


    content = f"The current stock price of {symbol} is ${price}"
    content += f"\n The price has changed by ${change} today  {emoji}"

    embed = discord.Embed(color=color,
                          title=f"{emoji}  Stock Price of `{symbol}` is ${price}",
                          description=f"The price has changed by ${change} today.")

    await interaction.edit_original_response(embed=embed)
