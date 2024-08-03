#!/usr/bin/env python3
import discord


async def retirement(
    ctx, startingage, startingcash, yearlysavings, desiredincome, growthrate
):

    # Initial Response
    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    sustainingyear = 0
    halfwaymoney = 0
    midage = 0
    ageset = False
    age = startingage
    money = startingcash
    growthrate = (growthrate / 100) + 1

    while age < 60:
        money = (money + yearlysavings) * growthrate
        annualdividends = money * 0.04

        midage = int(((60 - age) / 2) + (startingage))

        if age == midage:
            halfwaymoney = money

        if annualdividends >= desiredincome and ageset is False:
            sustainingyear = str(age)
            ageset = True
        age = age + 1

    if sustainingyear == 0:
        sustainingyear = str("You'll be dead, buddy")

    content = f"Investment value at 60 years old => {str(format(money, ',d'))} \n"
    content += (
        f"Annual dividends at 60 years old => {str(format(annualdividends, ',d'))} \n"
    )
    content += f"Age you can live off dividends => {str(sustainingyear)} \n"
    content += f"Investment value halfway to retirement => {str(halfwaymoney)} \n"

    embed = discord.Embed(
        color=0xD89B82,
        title="📈 Retirement",
        description=content,
    )

    await interaction.edit_original_response(embed=embed)
