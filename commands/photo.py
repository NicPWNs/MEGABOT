#!/usr/bin/env python3
import os
import boto3
import random
import discord


async def photo(ctx):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Posting Random Photo...")
    interaction = await ctx.respond(embed=embed)

    TABLE = "discord-photos"
    ddb = boto3.resource("dynamodb")
    table = ddb.Table(TABLE)

    data = table.scan()["Items"]
    name = random.choice(data)["name"]

    url = boto3.client("s3").generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": str(os.getenv("PHOTO_BUCKET")), "Key": name},
        ExpiresIn=604800,
    )

    embed = discord.Embed(color=0xFFCC4D, title="📸  Random Photo").set_image(url=url)
    await interaction.edit_original_response(embed=embed)
