#!/usr/bin/env python3
import megacoin
import discord


async def payout(ctx, user, amount, message):

    guild = discord.utils.get(ctx.bot.guilds, name="MEGACORD")
    role = discord.utils.get(guild.roles, name="MEGAPAYERS")

    if not role in ctx.user.roles:

        embed = discord.Embed(color=0xffcd4c, title="🏆  Payout",
                              description=f"🤡  Nice try <@{ctx.user.id}>.")
        await ctx.respond(embed=embed)
        return

    description = "Sending Payout..."
    embed = discord.Embed(
        color=0xffcd4c, title="🏆  Payout", description=description)
    interaction = await ctx.respond(embed=embed)

    await megacoin.add(user, amount)

    description = f"**<@{user.id}> Earned {str(amount)} <:MEGACOIN:1090620048621707324>.**\n\n{message}"

    embed = discord.Embed(
        color=0xffcd4c, title="🏆  Payout", description=description).set_thumbnail(url=user.display_avatar)
    await interaction.edit_original_response(embed=embed)
