#!/usr/bin/env python3
import megacoin
import discord
import boto3


async def bank(ctx):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Loading...")
    interaction = await ctx.respond(embed=embed)

    TABLE = "discord-megacoin"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    data = table.scan()['Items']

    entry = 1
    description = ""

    data = sorted(data, key=lambda d: d['coins'], reverse=True)

    for item in data:
        if not int(item['coins']) == 0:
            description += f"{entry}. <@{item['id']}> with {item['coins']} <:MEGACOIN:1090620048621707324>\n"
        entry += 1

    embed = discord.Embed(
        color=0xfee9b6, title="💰  MEGACOIN LEADERBOARD", description=description)
    interaction = await ctx.respond(embed=embed)
