#!/usr/bin/env python3
import discord


async def poll(ctx, question, option1, option2, option3=None, option4=None, option5=None, option6=None, option7=None, option8=None, option9=None):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    options = [option1, option2, option3, option4, option5, option6, option7, option8, option9]
    numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    description = ""
    optionCount = 0

    for option in options:
        if option:
            description += "\n" + numbers[optionCount] + ".  " + option
            optionCount += 1

    embed = discord.Embed(color=0xffd983,
                          title=f"🗳️  Poll:  {question}",
                          description=description
                          )

    message = await interaction.edit_original_response(embed=embed)

    for count in range(optionCount):
        await message.add_reaction(numbers[count])
