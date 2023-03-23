#!/usr/bin/env python3
import os
import time
import discord
from dotenv import load_dotenv
from random import random
from random_unicode_emoji import random_emoji

from slash_commands.age import age
from slash_commands.bless import bless
from slash_commands.chat import chat
from slash_commands.code import code
from slash_commands.coin import coin
from slash_commands.csgo import csgo
from slash_commands.dice import dice
from slash_commands.emote import emote
from slash_commands.image import image
from slash_commands.kanye import kanye
from slash_commands.kill import kill
from slash_commands.math import math
from slash_commands.nasa import nasa
from slash_commands.pause import pause
from slash_commands.ping import ping
from slash_commands.play import play
from slash_commands.random_unicode_emoji import random_unicode_emoji
from slash_commands.retirement import retirement
from slash_commands.resume import resume
from slash_commands.stock import stock
from slash_commands.stop import stop
from slash_commands.streak import streak
from slash_commands.test import test


if __name__ == "__main__":

    startTime = time.time()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD_ID = os.getenv('DISCORD_GUILD_ID')

    bot = discord.Bot(intents=discord.Intents.all())
    guild = discord.utils.get(bot.guilds, name="MEGACORD")

    @bot.listen('on_message')
    async def on_message(message):

        if 'testing event listeners...' in message.content.lower():
            await message.edit('\n\n✅ MEGABOT Testing Done!')

        if message.author == bot.user:
            return

        try:
            if random() < .25:
                emojis = await guild.fetch_emojis()
                for _ in range(0,5):
                    emojis = emojis + emojis
                await message.add_reaction(random_emoji(custom=emojis)[0])

        except:
            pass

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

    @bot.slash_command(name="ping", description="Responds with pong.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await ping(ctx)

    @bot.slash_command(name="age", description="Guesses the age of a specified name.", guild_ids=[GUILD_ID])
    @discord.option(
        name="name",
        description="Name to guess age of.",
        input_type=str,
        required=True
    )
    async def call(ctx, name):
        await age(ctx, name)

    @bot.slash_command(name="math", description="Evaluate provided math expression.", guild_ids=[GUILD_ID])
    @discord.option(
        name="expression",
        description="Expression to evaluate.",
        input_type=str,
        required=True
    )
    async def call(ctx, expression):
        await math(ctx, expression)

    @bot.slash_command(name="bless", description="Blesses the mess!", guild_ids=[GUILD_ID])
    async def call(ctx):
        await bless(ctx)

    @bot.slash_command(name="chat", description="Chat with MEGABOT.", guild_ids=[GUILD_ID])
    @discord.option(
        name="prompt",
        description="Prompt for MEGABOT to respond to.",
        input_type=str,
        required=True
    )
    async def call(ctx, prompt):
        await chat(ctx, prompt)

    @bot.slash_command(name="nasa", description="Retrieve the NASA photo of the day.", guild_ids=[GUILD_ID])
    @discord.option(
        name="details",
        description="Provide the explanation of the photo.",
        input_type=bool,
        required=False,
        choices=["True", "False"]
    )
    async def call(ctx, details):
        await nasa(ctx, details)

    @bot.slash_command(name="kanye", description="Retrieve a random Kanye West quote.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await kanye(ctx)

    @bot.slash_command(name="csgo", description="Retrieve CS:GO stats.", guild_ids=[GUILD_ID])
    @discord.option(
        name="username",
        description="User on Steam, a Steam ID, Steam Community URI, or Steam Vanity Username.",
        input_type=str,
        required=True
    )
    async def call(ctx, username):
        await csgo(ctx, username)

    @bot.slash_command(name="streak", description="Keep a daily streak going!", guild_ids=[GUILD_ID])
    @discord.option(
        name="stats",
        description="Get streak stats.",
        input_type=bool,
        required=False,
        choices=["True", "False"]
    )
    async def call(ctx, stats):
        await streak(ctx, stats)

    @bot.slash_command(name="test", description="Test MEGABOT.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await test(ctx, startTime)

    @bot.slash_command(name="kill", description="Stop MEGABOT. (Admin Only)", guild_ids=[GUILD_ID])
    async def call(ctx):
        await kill(ctx)

    @bot.slash_command(name="play", description="Plays music.", guild_ids=[GUILD_ID])
    @discord.option(
        name="search",
        description="Song to search for on YouTube.",
        input_type=str,
        required=True
    )
    async def call(ctx, search):
        await play(ctx, search)

    @bot.slash_command(name="stop", description="Stops music.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await stop(ctx)

    @bot.slash_command(name="pause", description="Pauses music.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await pause(ctx)

    @bot.slash_command(name="resume", description="Resumes music.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await resume(ctx)

    @bot.slash_command(name="emote", description="Resumes music.", guild_ids=[GUILD_ID])
    @discord.option(
        name="search",
        description="Emote to search for.",
        input_type=str,
        required=True
    )
    @discord.option(
        name="add",
        description="Add emote to server?",
        input_type=bool,
        required=False,
        choices=["True", "False"]
    )
    async def call(ctx, search, add):
        await emote(ctx, search, add)

    @bot.slash_command(name="stock", description="Searches a stock price.", guild_ids=[GUILD_ID])
    @discord.option(
        name="symbol",
        description="Stock symbol to search for (ie. PLTR).",
        input_type=str,
        required=True
    )
    async def call(ctx, symbol):
        await stock(ctx, symbol)

    @bot.slash_command(name="retirement", description="Retirement calculator for your planning pleasure.", guild_ids=[GUILD_ID])
    @discord.option(
        name="age",
        description="How old are you?",
        input_type=int,
        required=True
    )
    @discord.option(
        name="startingcash",
        description="Current investments",
        input_type=int,
        required=True
    )
    @discord.option(
        name="yearlysavings",
        description="Money saved each year",
        input_type=int,
        required=True
    )
    @discord.option(
        name="desiredincome",
        description="Desired yearly income at retirement",
        input_type=int,
        required=True
    )
    @discord.option(
        name="growthrate",
        description="Optimistic => %, Expected => %, Conservative => % ",
        input_type=int,
        required=True
    )
    async def call(ctx, age, startingcash, yearlysavings, desiredincome, growthrate):
        await retirement(ctx, age, startingcash, yearlysavings, desiredincome, growthrate)

    @bot.slash_command(name="coin", description="Flip a coin.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await coin(ctx)

    @bot.slash_command(name="dice", description="Roll a dice.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await dice(ctx)

    @bot.slash_command(name="image", description="Generate an image with AI.", guild_ids=[GUILD_ID])
    @discord.option(
        name="prompt",
        description="Prompt for image to be generated from.",
        input_type=str,
        required=True
    )
    async def call(ctx, prompt):
        await image(ctx, prompt)

    @bot.slash_command(name="code", description="Write code with AI.", guild_ids=[GUILD_ID])
    @discord.option(
        name="prompt",
        description="Prompt for code to be written from.",
        input_type=str,
        required=True
    )
    async def call(ctx, prompt):
        await code(ctx, prompt)

    @bot.slash_command(name="random-unicode-emoji", description="Return a random Unicode emoji.", guild_ids=[GUILD_ID])
    async def call(ctx):
        await random_unicode_emoji(ctx)

    bot.run(TOKEN)
