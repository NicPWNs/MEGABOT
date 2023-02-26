#!/usr/bin/env python3
import discord


async def on_member_join(member, bot):

    guild = discord.utils.get(bot.guilds, name="MEGACORD")

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

    channel = discord.utils.get(guild.channels, name="main")

    await channel.send(f"I'm watching you <@{member.id}>")
