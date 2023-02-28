#!/usr/bin/env python3
# inputs are as follows
#

async def retirement(ctx, age, startingcash, yearlysavings, desiredincome, growthrate):
    money = startingcash
    growthrate = (growthrate / 100) + 1
    ageset = False
    while age < 60:
        money = (money + yearlysavings) * growthrate
        annualdividends = money * .04

        if age == (60-age)/2:
            halfwaymoney = money
        # PROBLEM PROBLEM PROBLEM, annualdividends will never exactly equal desiredincome
        if annualdividends >= desiredincome and ageset is False:
            sustainingyear = age
            ageset = True
        age = age + 1
    investmentworth = money

    # outputs variables are as follows
    # investmentworth => value of investments at 60 years
    # halfwaymoney => value of investments halfway to retirement
    # annualdividends => annual $ from dividends from investments
    # sustainingyear => user's age when desired yearly income
    #                   is met by investment dividends.

    content = f"Investment value at 60 years old => {str(investmentworth)} \n"
    content += f"Annual Dividends at 60 years old => {str(annualdividends)} \n"
    content += f"Age you can live off dividends => {str(sustainingyear)} \n"
    content += f"Investment value halfway to retirement => {str(halfwaymoney)} \n"
    await ctx.respond(content=content)
