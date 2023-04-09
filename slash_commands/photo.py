#!/usr/bin/env python3
import boto3
import random
import discord


async def photo(ctx):

    embed = discord.Embed(
        color=0xfee9b6, title="⏳  Posting Random Photo...")
    interaction = await ctx.respond(embed=embed)

    TABLE = "discord-photos"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    data = table.scan()['Items']
    photo = random.choice(data)['photo']

    embed = discord.Embed(
        color=0xffcc4d, title="📸  Random Photo").set_image(url=photo)
    await interaction.edit_original_response(embed=embed)
