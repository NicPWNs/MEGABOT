#!/usr/bin/env python3
import os
import boto3
import discord


async def upload(ctx, photo):

    embed = discord.Embed(color=0xFEE9B6, title="⏳  Uploading...")
    interaction = await ctx.respond(embed=embed)

    if photo.content_type not in [
        "image/jpeg",
        "image/png",
        "image/heic",
        "video/quicktime",
        "video/mp4",
    ]:
        embed = discord.Embed(
            color=0xDD2F45,
            title="❌ Error",
            description=f"File Type `{photo.content_type}` is Not Supported!",
        )
        await interaction.edit_original_response(embed=embed)
        return

    s3 = boto3.client("s3")
    file = await photo.to_file()
    s3.upload_fileobj(file.fp, str(os.getenv("PHOTO_BUCKET")), photo.filename)

    TABLE = "discord-photos"
    ddb = boto3.resource("dynamodb")
    table = ddb.Table(TABLE)

    table.put_item(
        Item={
            "id": str(photo.id),
            "name": str(photo.filename),
            "type": str(photo.content_type),
        }
    )

    embed = discord.Embed(color=0xC0DEF4, title="🎞️  Photo Uploaded!").set_image(
        url=photo.url
    )
    await interaction.edit_original_response(embed=embed)
