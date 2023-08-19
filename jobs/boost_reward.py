#!/usr/bin/env python3
import discord
import time
import datetime
import modules.megacoin as megacoin


async def boost_reward(bot, startTime):

    runTime = int(time.time() - startTime)
    if runTime < 60:
        return

    d = datetime.datetime.now()
    date = int(d.strftime("%d"))

    if date == 1:
        guild = discord.utils.get(bot.guilds, name="MEGACORD")
        channel = discord.utils.get(guild.channels, name="main")
        boosters = guild.premium_subscribers

        coins = 250

        for booster in boosters:
            await megacoin.add(booster, coins)
            await channel.send(
                f"<:boost:1090737525607379025>  Thank you for boosting the MEGACORD this month <@{booster.id}>! + {coins} <:MEGACOIN:1090620048621707324>")
    else:
        return
