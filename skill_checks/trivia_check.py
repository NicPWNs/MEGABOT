#!/usr/bin/env python3
import time
import random
import discord
import requests
import megacoin


async def trivia_check(bot, startTime):

    def check(reaction, user):
        if reaction.message.channel == channel:
            if reaction.emoji in ['🇦', '🇧', '🇨', '🇩']:
                if user not in answered:
                    answered.append(user)
                    if reaction.emoji == choices[index]:
                        return True

    runTime = int(time.time() - startTime)
    if runTime < 60:
        return

    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="casino")

    r = requests.get(
        "https://the-trivia-api.com/api/questions?limit=1&region=US").json()

    question = r[0]['question']
    answers = []
    correct = r[0]['correctAnswer']
    answers.append(correct)
    for answer in r[0]['incorrectAnswers']:
        answers.append(answer)
    random.shuffle(answers)
    index = answers.index(correct)
    answered = [bot.user]

    description = f"Anyone can answer within 10 minutes for <:MEGACOIN:1090620048621707324> *x10*. One guess only!\n\n"

    choices = ['🇦', '🇧', '🇨', '🇩']
    num = 0
    for answer in answers:
        description += f"{choices[num]}   {answer}\n"
        num += 1

    embed = discord.Embed(color=0xbf1930,
                          title=f"❓  Trivia: {question}",
                          description=description
                          ).set_author(name="🎯  Skill Check!")
    try:
        message = await channel.send(embed=embed)
        await message.add_reaction('🇦')
        await message.add_reaction('🇧')
        await message.add_reaction('🇨')
        await message.add_reaction('🇩')
    except discord.errors.Forbidden:
        return

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=600, check=check)
        await reaction.remove(user)
        await message.clear_reactions()
    except:
        text = f"❌ No one guessed correctly within 10 minutes!"
        embed = embed.set_footer(
            text=text, icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/thumbnail.gif")
        await message.edit(embed=embed)
        await message.clear_reactions()
        return

    text = f"+ 10 ✅ {user.display_name} Wins! The answer was {choices[index]}"
    await megacoin.add(user, 10)

    embed = embed.set_footer(
        text=text, icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
    await message.edit(embed=embed)
