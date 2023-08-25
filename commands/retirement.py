#!/usr/bin/env python3


async def retirement(ctx, age, startingcash, yearlysavings, desiredincome, growthrate):

    sustainingyear = 0
    halfwaymoney = 0
    testage = 0
    ageset = False
    startingage = int(age)
    age = int(age)
    startingcash = float(startingcash)
    yearlysavings = float(yearlysavings)
    desiredincome = float(desiredincome)
    growthrate = float(growthrate)

    money = startingcash

    growthrate = (growthrate / 100) + 1

    while age < 60:
        money = (money + yearlysavings) * growthrate
        annualdividends = money * .04

        testage = int(((60-age)/2) + (startingage))

        if age == testage:
            halfwaymoney = money

        if annualdividends >= desiredincome and ageset is False:
            sustainingyear = str(age)
            ageset = True
        age = age + 1
    investmentworth = money

    # outputs variables are as follows
    # investmentworth => value of investments at 60 years
    # halfwaymoney => value of investments halfway to retirement
    # annualdividends => annual $ from dividends from investments
    # sustainingyear => user's age when desired yearly income
    #                   is met by investment dividends.

    if sustainingyear == 0:
        sustainingyear = str("you'll be dead, buddy")

    content = f"_______________ \n Investment value at 60 years old => {str(format(int(investmentworth), ',d'))} \n"
    content += f"Annual Dividends at 60 years old => {str(format(int(annualdividends), ',d'))} \n"
    content += f"Age you can live off dividends => {str(sustainingyear)} \n"
    content += f"Investment value halfway to retirement => {str(int(halfwaymoney))} \n"
    # content += f"Age {str(testage)}"  # USED FOR TESTING.
    await ctx.respond(content=content)
