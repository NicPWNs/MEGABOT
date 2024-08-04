#!/usr/bin/env python3
import discord


async def retirement(ctx, age, cash, yearlysavings, desiredincome, growthrate):

    # Initial Response
    embed = discord.Embed(color=0xFEE9B6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    # Initalize Variables
    sustainingage = 0
    halfwaymoney = 0
    ageset = False
    growthrate = (growthrate / 100) + 1
    midage = int(((60 - age) / 2) + (age))

    # Run Calculations
    while age < 60:
        cash = (cash + yearlysavings) * growthrate
        annualdividends = cash * 0.04

        if age == midage:
            halfwaymoney = cash

        if annualdividends >= desiredincome and ageset is False:
            sustainingage = age
            ageset = True

        age = age + 1

    # Check Retirement Goals
    if sustainingage == 0:
        sustainingage = str("You'll be dead, buddy...")

    # Return Results
    content = f"**Investment value at 60 years old:** ${cash:,.2f}\n"
    content += f"**Annual dividends at 60 years old:** ${annualdividends:,.2f}\n"
    content += f"**Age you can live off dividends:** {sustainingage}\n"
    content += f"**Investment value halfway to retirement (Age {midage}):** ${halfwaymoney:,.2f}\n"

    embed = discord.Embed(
        color=0xDD2E44,
        title="📈 Retirement",
        description=content,
    )

    await interaction.edit_original_response(embed=embed)
