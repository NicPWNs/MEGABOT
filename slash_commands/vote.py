#!/usr/bin/env python3
import time
import random
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

    if datetime.now().date() == data['Item']['date']:
        embed = discord.Embed(
        color=0x5965f3, title="🗳️  MEGABOT Voting", description="You've already voted today!")
        await interaction.edit_original_response(embed=embed)
        return

    # OBFUSCATE THE LINK EVENTUALLY

    embed = discord.Embed(
        color=0x5965f3, title="🗳️  MEGABOT Voting", description="[Click here](http://adfoc.us/8239381) to vote.")
    await interaction.edit_original_response(embed=embed)

    table.put_item(
        Item={
            'id': str(ctx.user.id),
            'date': str(datetime.now().date())
        }
    )

    time.sleep(random.randint(180, 300))

    await megacoin.add(ctx.user, 100)

    embed = discord.Embed(
        color=0x5965f3, title="🗳️  MEGABOT Voting", description="Vote registered! +100 <:MEGACOIN:1090620048621707324>")
    await interaction.edit_original_response(embed=embed)
