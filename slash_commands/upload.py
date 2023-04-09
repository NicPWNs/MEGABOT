#!/usr/bin/env python3
import boto3
import discord


async def upload(ctx, photo):

    embed = discord.Embed(color=0xfee9b6, title="⏳  Uploading...")
    interaction = await ctx.respond(embed=embed)

    if photo.content_type not in ["image/jpeg", "image/png"]:
        embed = discord.Embed(color=0xdd2f45, title="❌ Error", description="Only JPEG/JPG and PNG Images are Supported!"
                              ).set_image(url=photo.url)
        await interaction.edit_original_response(embed=embed)
        return

    TABLE = "discord-photos"
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(TABLE)

    table.put_item(
        Item={
            'id': str(photo.id),
            'photo': str(photo.url),
            'name': str(photo.filename),
            'type': str(photo.content_type)
        }
    )

    embed = discord.Embed(color=0xc0def4,
                          title="🎞️  Photo Uploaded!"
                          ).set_image(url=photo.url)
    await interaction.edit_original_response(embed=embed)
