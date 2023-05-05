#!/usr/bin/env python3
import os
import time
import boto3
import random
import discord


async def random_photo(bot, startTime):

    runTime = int(time.time() - startTime)
    if runTime < 60:
        return

    guild = discord.utils.get(bot.guilds, name="MEGACORD")
    channel = discord.utils.get(guild.channels, name="main")

    embed = discord.Embed(
        color=0xfee9b6, title="⏳  Posting Random Photo of the Day...")
    message = await channel.send(embed=embed)

    TABLE = "discord-photos"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    data = table.scan()['Items']
    name = random.choice(data)['name']

    url = boto3.client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': str(os.getenv('PHOTO_BUCKET')), 'Key': name},
        ExpiresIn=604800)

    embed = discord.Embed(
        color=0xffcc4d, title="🌞 Random Photo of the Day").set_image(url=url)
    await message.edit(embed=embed)
