#!/usr/bin/env python3
import os
import time
import spotdl
import random
import discord
import asyncio
import nest_asyncio
import datetime
from discord.ext import tasks
from dotenv import load_dotenv
from random_unicode_emoji import random_emoji
from skill_checks.album_check import album_check
from skill_checks.boost_check import boost_check
from slash_commands.age import age
from slash_commands.album import album
from slash_commands.balance import balance
from slash_commands.bank import bank
from slash_commands.bless import bless
from slash_commands.chat import chat
from slash_commands.code import code
from slash_commands.coin import coin
from slash_commands.csgo import csgo
from slash_commands.dice import dice
from slash_commands.double import double
from slash_commands.emote import emote
from slash_commands.image import image
from slash_commands.kanye import kanye
from slash_commands.kill import kill
from slash_commands.math import math
from slash_commands.nasa import nasa
from slash_commands.ping import ping
from slash_commands.play import play
from slash_commands.queue import queue
from slash_commands.randellium import randellium
from slash_commands.random_unicode_emoji import random_unicode_emoji
from slash_commands.retirement import retirement
from slash_commands.stock import stock
from slash_commands.stop import stop
from slash_commands.streak import streak
from slash_commands.test import test
from slash_commands.wheel import wheel


if __name__ == "__main__":

    startTime = time.time()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = os.getenv('DISCORD_GUILD_ID')

    bot = discord.Bot(intents=discord.Intents.all())
    guild = discord.utils.get(bot.guilds, name="MEGACORD")

    queued = []
    nest_asyncio.apply()
    SDL = spotdl.Spotdl(client_id=str(os.getenv('SPOTIFY_CLIENT')), client_secret=str(
        os.getenv('SPOTIFY_SECRET')), headless=True, loop=asyncio.get_event_loop())

    # Timed Events
    @tasks.loop(minutes=random.randint(120, 240))
    async def skill_check(bot):
        await album_check(bot)

    @tasks.loop(time=datetime.time.fromisoformat('09:00:00'))
    async def booster_check(bot):
        await boost_check(bot)

    # Event Listeners
    @bot.listen('on_ready')
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="You..."))
        skill_check.start(bot)
        booster_check.start(bot)

    @bot.listen('on_message')
    async def on_message(message):

        if 'testing event listeners...' in message.content.lower():
            await message.edit('\n\n✅ MEGABOT Testing Done!')

        if message.author == bot.user:
            return

        if random.random() < .2:
            guild = discord.utils.get(bot.guilds, name="MEGACORD")
            emojis = await guild.fetch_emojis()
            for _ in range(0, 6):
                emojis = emojis + emojis
            await message.add_reaction(random_emoji(custom=emojis)[0])

        if 'birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')

        if 'megabot' in message.content.lower():
            await message.channel.send('Hello there! 👋')

    @bot.listen('on_member_join')
    async def on_member_join(member):

        guild = discord.utils.get(bot.guilds, name="MEGACORD")

        role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
        await member.add_roles(role)

        channel = discord.utils.get(guild.channels, name="main")

        await channel.send(f"I'm watching you <@{member.id}>")

    # Slash Commands
    @bot.slash_command(name="age", description="Guesses the age of a specified name.", guild_ids=[GUILD_ID])
    async def call(ctx, name: discord.Option(discord.SlashCommandOptionType.string, description="Name to guess age of.", required=True)):
        await age(ctx, name)

    @bot.slash_command(name="album", description="Play an album artist guessing game.", guild_ids=[GUILD_ID])
    async def call(ctx, genre: discord.Option(description="Pick a genre. Hip-Hop is default.", default="hip-hop", choices=["hip-hop", "pop", "rock", "alternative", "hard-rock"])):
        await album(ctx, genre)

    @bot.slash_command(name="balance", description="View MEGACOIN balance.", guild_ids=[GUILD_ID])
    async def call(ctx, user: discord.Option(discord.SlashCommandOptionType.user, required=False, description="User to get the balance of.")):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**", ephemeral=True)
            return
        await balance(ctx, user)

    @bot.slash_command(name="bank", description="View the MEGACOIN balance leaderboard.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await bank(ctx)

    @bot.slash_command(name="bless", description="Blesses the mess!", guild_ids=[GUILD_ID])
    async def call(ctx):
        await bless(ctx)

    @bot.slash_command(name="chat", description="Chat with MEGABOT.", guild_ids=[GUILD_ID])
    async def call(ctx, prompt: discord.Option(discord.SlashCommandOptionType.string, description="Prompt for MEGABOT to respond to.", required=True)):
        await chat(ctx, prompt)

    @bot.slash_command(name="code", description="Write code with AI.", guild_ids=[GUILD_ID])
    async def call(ctx, prompt: discord.Option(discord.SlashCommandOptionType.string, description="Prompt for code to be written from.", required=True)):
        await code(ctx, prompt)

    @bot.slash_command(name="coin", description="Flip a coin.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await coin(ctx)

    @bot.slash_command(name="csgo", description="Retrieve CS:GO stats.", guild_ids=[GUILD_ID])
    async def call(ctx, username: discord.Option(discord.SlashCommandOptionType.string, description="User on Steam, a Steam ID, Steam Community URI, or Steam Vanity Username.", required=True)):
        await csgo(ctx, username)

    @bot.slash_command(name="dice", description="Roll a dice.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await dice(ctx)

    @bot.slash_command(name="double", description="Play MEGACOIN double or nothing.", guild_ids=[GUILD_ID])
    async def call(ctx, confirm: discord.Option(discord.SlashCommandOptionType.boolean, required=True, description="Confirm you want to double or nothing your entire MEGACOIN balance.")):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**", ephemeral=True)
            return
        await double(ctx, confirm)

    @bot.slash_command(name="emote", description="Search for a 7TV emote.", guild_ids=[GUILD_ID])
    async def call(ctx,
                   search: discord.Option(discord.SlashCommandOptionType.string, description="Emote to search for.", required=True),
                   add: discord.Option(discord.SlashCommandOptionType.boolean, description="Add emote to server?", required=False),
                   id: discord.Option(discord.SlashCommandOptionType.boolean, description="Search by 7TV emote ID.", required=False)):
        await emote(ctx, search, add, id)

    @bot.slash_command(name="image", description="Generate an image with AI.", guild_ids=[GUILD_ID])
    async def call(ctx, prompt: discord.Option(discord.SlashCommandOptionType.string, description="Prompt for image to be generated from.", required=True)):
        await image(ctx, prompt)

    @bot.slash_command(name="kanye", description="Retrieve a random Kanye West quote.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await kanye(ctx)

    @bot.slash_command(name="kill", description="Stop MEGABOT. (Admin Only)", guild_ids=[GUILD_ID])
    async def call(ctx):
        await kill(ctx)

    @bot.slash_command(name="math", description="Evaluate provided math expression.", guild_ids=[GUILD_ID])
    async def call(ctx, expression: discord.Option(discord.SlashCommandOptionType.string, description="Expression to evaluate.", required=True)):
        await math(ctx, expression)

    @bot.slash_command(name="nasa", description="Retrieve the NASA photo of the day.", guild_ids=[GUILD_ID])
    async def call(ctx, details: discord.Option(discord.SlashCommandOptionType.boolean, description="Provide the explanation of the photo.", required=False)):
        await nasa(ctx, details)

    @bot.slash_command(name="ping", description="Responds with pong.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await ping(ctx)

    @bot.slash_command(name="play", description="Plays music.", guild_ids=[GUILD_ID])
    async def call(ctx, search: discord.Option(discord.SlashCommandOptionType.string, description="Song to search for on YouTube.", required=True)):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**", ephemeral=True)
            return
        await play(ctx, search, queued, SDL, skip=False)

    @bot.slash_command(name="queue", description="Show the current music queue.", guild_ids=[GUILD_ID])
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**", ephemeral=True)
            return
        await queue(ctx, queued)

    @bot.slash_command(name="randellium", description="Code Breaker", guild_ids=[GUILD_ID])
    async def call(ctx):
        await randellium(ctx)

    @bot.slash_command(name="random-unicode-emoji", description="Return a random Unicode emoji. No Discord emojis.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await random_unicode_emoji(ctx)

    @bot.slash_command(name="retirement", description="Retirement calculator for your planning pleasure.", guild_ids=[GUILD_ID])
    async def call(ctx,
                   age: discord.Option(discord.SlashCommandOptionType.integer, description="How old are you?", required=True),
                   startingcash: discord.Option(discord.SlashCommandOptionType.integer, description="Current investments.", required=True),
                   yearlysavings: discord.Option(discord.SlashCommandOptionType.integer, description="Money saved each year.", required=True),
                   desiredincome: discord.Option(discord.SlashCommandOptionType.integer, description="Desired yearly income at retirement.", required=True),
                   growthrate: discord.Option(discord.SlashCommandOptionType.integer, description="Optimistic => %, Expected => %, Conservative => %", required=True)):
        await retirement(ctx, age, startingcash, yearlysavings, desiredincome, growthrate)

    @bot.slash_command(name="skip", description="Skip the current song.", guild_ids=[GUILD_ID])
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**", ephemeral=True)
            return
        search = ""
        await play(ctx, search, queued, SDL, skip=True)

    @bot.slash_command(name="stock", description="Searches a stock price.", guild_ids=[GUILD_ID])
    async def call(ctx, symbol: discord.Option(discord.SlashCommandOptionType.string, description="Stock symbol to search for (ie. PLTR).", required=True)):
        await stock(ctx, symbol)

    @bot.slash_command(name="stop", description="Stops music.", guild_ids=[GUILD_ID])
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**", ephemeral=True)
            return
        await stop(ctx, queued)

    @bot.slash_command(name="streak", description="Keep a daily streak going!", guild_ids=[GUILD_ID])
    async def call(ctx, stats: discord.Option(discord.SlashCommandOptionType.boolean, description="Get streak stats.", required=False)):
        if not (ctx.channel.name == "streaks" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1022570321930358895>**", ephemeral=True)
            return
        await streak(ctx, stats)

    @bot.slash_command(name="test", description="Test MEGABOT.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await test(ctx, startTime)

    @bot.slash_command(name="wheel", description="Spin the MEGACOIN wheel.", guild_ids=[GUILD_ID])
    async def call(ctx, wager: discord.Option(discord.SlashCommandOptionType.integer, required=True, description="Amount you want to wager on the MEGACOIN wheel.")):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**", ephemeral=True)
            return
        await wheel(ctx, wager)

    bot.run(TOKEN)
