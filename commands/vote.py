#!/usr/bin/env python3
import time
import boto3
import discord
from datetime import datetime
import modules.megacoin as megacoin


async def vote(ctx):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    TABLE = "discord-vote"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    data = table.get_item(
        Key={
            'id': str(ctx.user.id)
        }
    )

    dataLength = int(data['ResponseMetadata']
                     ['HTTPHeaders']['content-length'])

    if dataLength > 5:
        if str(datetime.now().date()) == data['Item']['date']:
            embed = discord.Embed(
                color=0x5965f3, title="🗳️  MEGABOT Voting", description="You've already voted today!")
            await interaction.edit_original_response(embed=embed)
            return

    # OBFUSCATE THE LINK EVENTUALLY

    embed = discord.Embed(
        color=0x5965f3, title="🗳️  MEGABOT Voting", description="[Click here](http://adfoc.us/82393897415395) to vote.").set_footer(text="Click 'skip' top-right!")
    await interaction.edit_original_response(embed=embed)

    table.put_item(
        Item={
            'id': str(ctx.user.id),
            'username': str(ctx.user.name),
            'voted': str("false")
        }
    )

    voted = False
    timePassed = 0

    # Check every ten seconds if user voted
    while voted is False:
        time.sleep(10)
        timePassed += 10
        data = table.get_item(
            Key={
                'id': str(ctx.user.id)
            }
        )
        voted = data['Item']['voted']
        if timePassed >= 120:
            embed = discord.Embed(
                color=0x5965f3, title="🗳️  MEGABOT Voting", description="You took too long to vote! Try again.")
            await interaction.edit_original_response(embed=embed)
            return

    table.put_item(
        Item={
            'id': str(ctx.user.id),
            'date': str(datetime.now().date()),
            'username': str(ctx.user.name),
            'voted': str("false")
        }
    )

    await megacoin.add(ctx.user, 50)

    embed = discord.Embed(
        color=0x5965f3, title="🗳️  MEGABOT Voting", description="Vote registered! +50 <:MEGACOIN:1090620048621707324>")
    await interaction.edit_original_response(embed=embed)
