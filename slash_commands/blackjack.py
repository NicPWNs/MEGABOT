#!/usr/bin/env python3
import time
import discord
import random
import megacoin


def get_card(ctx):
    card = random.choice(['2', '3', '4', '5', '6', '7',
                          '8', '9', '10', 'j', 'q', 'k', 'a']) + random.choice(['c', 'd', 'h', 's'])
    emoji = discord.utils.get(ctx.guild.emojis, name=card)
    return emoji


def hand_value(dealt):
    total = 0

    for card in dealt:
        if card.name[0] in ['j', 'q', 'k'] or card.name[1] == '0':
            value = 10
        elif card.name[0] == 'a':
            value = 11
        else:
            value = int(card.name[0])
        total += value

    for card in dealt:
        if total > 21:
            if card.name[0] == 'a':
                total -= 10

    return total


async def blackjack(ctx, wager):

    def check(msg):
        guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
        channel = discord.utils.get(guild.channels, name="casino")
        if msg.channel == channel:
            if msg.author == ctx.user:
                if msg.content.lower() in ["hit", "stand"]:
                    return True

    balance = await megacoin.balance(ctx.user)

    if wager < 0:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description="🤡  Nice try.")
        await ctx.respond(embed=embed)
        return
    elif balance == 0:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description="You have 0 <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return
    elif balance < wager:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"You don't have {str(wager)} <:MEGACOIN:1090620048621707324>")
        await ctx.respond(embed=embed)
        return

    embed = discord.Embed(
        color=0x9366cd, title="🃏  Blackjack", description="Dealing...")
    interaction = await ctx.respond(embed=embed)

    dealerText = "*Dealer* "
    dealerLabel = await ctx.channel.send(dealerText)

    dealerDealt = ['']
    playerDealt = ['']
    card = ''

    while card in dealerDealt or card in playerDealt:
        card = get_card(ctx)
    dealerDealt.append(card)
    dealerHand = str(card)
    dealer = await ctx.channel.send(dealerHand)
    while card in dealerDealt or card in playerDealt:
        card = get_card(ctx)
    dealerDealt.append(card)
    dealerHand += str(discord.utils.get(ctx.guild.emojis, name="MEGACARD"))
    await dealer.edit(dealerHand)
    dealerDealt.remove('')
    dealerValue = hand_value(dealerDealt)
    await dealerLabel.edit(dealerText + "(?)")

    playerText = "*Player* "
    playerLabel = await ctx.channel.send(playerText)

    while card in dealerDealt or card in playerDealt:
        card = get_card(ctx)
    playerDealt.append(card)
    playerHand = str(card)
    player = await ctx.channel.send(playerHand)
    while card in dealerDealt or card in playerDealt:
        card = get_card(ctx)
    playerDealt.append(card)
    playerHand += str(card)
    await player.edit(playerHand)
    playerDealt.remove('')
    playerValue = hand_value(playerDealt)
    await playerLabel.edit(playerText + f"({playerValue})")

    time.sleep(0)

    if playerValue == 21 and dealerValue == 21:
        dealerHand = dealerHand.replace(
            "<:MEGACARD:1091828635138281482>", str(dealerDealt[1]))
        await dealer.edit(dealerHand)
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"➡️  Push! <@{ctx.bot.user.id}> and <@{ctx.user.id}> both have Blackjack!").set_footer(
            text=f"+ 0", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await dealerLabel.edit(dealerText + f"({dealerValue})")
        return
    elif playerValue == 21:
        dealerHand = dealerHand.replace(
            "<:MEGACARD:1091828635138281482>", str(dealerDealt[1]))
        await dealer.edit(dealerHand)
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"✅  Win! <@{ctx.user.id}> has Blackjack!").set_footer(
            text=f"+ {str(wager * 1.5)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await megacoin.add(ctx.user, wager * 1.5)
        return
    elif dealerValue == 21:
        dealerHand = dealerHand.replace(
            "<:MEGACARD:1091828635138281482>", str(dealerDealt[1]))
        await dealer.edit(dealerHand)
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"❌  Lose! <@{ctx.bot.user.id}> has Blackjack!").set_footer(
            text=f"- {str(wager)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await dealerLabel.edit(dealerText + f"({dealerValue})")
        await megacoin.subtract(ctx.user, wager)
        return

    embed = discord.Embed(
        color=0x9366cd, title="🃏  Blackjack", description=f"Hit or Stand?")
    await interaction.edit_original_response(embed=embed)

    choice = "hit"
    msg = await ctx.bot.wait_for("message", timeout=600, check=check)
    choice = msg.content.lower()

    while playerValue < 21 and choice == "hit":
        while card in dealerDealt or card in playerDealt:
            card = get_card(ctx)
        playerDealt.append(card)
        playerHand += str(card)
        await player.edit(playerHand)
        playerValue = hand_value(playerDealt)
        await playerLabel.edit(playerText + f"({playerValue})")
        if playerValue > 21:
            break
        msg = await ctx.bot.wait_for("message", timeout=600, check=check)
        choice = msg.content.lower()

    if playerValue > 21:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"❌  Lose! <@{ctx.user.id}> busted with {str(playerValue)}!").set_footer(
            text=f"- {str(wager)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        dealerHand = dealerHand.replace(
            "<:MEGACARD:1091828635138281482>", str(dealerDealt[1]))
        await dealer.edit(dealerHand)
        await dealerLabel.edit(dealerText + f"({dealerValue})")
        await megacoin.subtract(ctx.user, wager)
        return

    embed = discord.Embed(
        color=0x9366cd, title="🃏  Blackjack", description=f"Stand! Revealing...")
    await interaction.edit_original_response(embed=embed)
    dealerHand = dealerHand.replace(
        "<:MEGACARD:1091828635138281482>", str(dealerDealt[1]))
    await dealer.edit(dealerHand)
    await dealerLabel.edit(dealerText + f"({dealerValue})")

    while dealerValue < 17:
        time.sleep(1)
        while card in dealerDealt or card in playerDealt:
            card = get_card(ctx)
        dealerDealt.append(card)
        dealerHand += str(card)
        await dealer.edit(dealerHand)
        dealerValue = hand_value(dealerDealt)
        await dealerLabel.edit(dealerText + f"({dealerValue})")
        if dealerValue > 17:
            break

    if dealerValue > 21:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"✅  Win! <@{ctx.bot.user.id}> busted!").set_footer(
            text=f"+ {str(wager)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await megacoin.add(ctx.user, wager)
        return
    elif playerValue > dealerValue:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"✅  Win! <@{ctx.user.id}> beats <@{ctx.bot.user.id}>!").set_footer(
            text=f"+ {str(wager)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await megacoin.add(ctx.user, wager)
        return
    elif dealerValue > playerValue:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"❌  Lose! <@{ctx.bot.user.id}> beats <@{ctx.user.id}>!").set_footer(
            text=f"- {str(wager)}", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        await megacoin.subtract(ctx.user, wager)
        return
    elif dealerValue == playerValue:
        embed = discord.Embed(
            color=0x9366cd, title="🃏  Blackjack", description=f"➡️  Push! <@{ctx.bot.user.id}> and <@{ctx.user.id}> are even.").set_footer(
            text=f"+ 0", icon_url="https://raw.githubusercontent.com/NicPWNs/MEGABOT/main/images/MEGACOIN.png")
        await interaction.edit_original_response(embed=embed)
        return
