#!/usr/bin/env python3
import os
import time
import spotdl
import random
import discord
import logging
import asyncio
import nest_asyncio
import datetime
from discord.ext import tasks
from dotenv import load_dotenv
from modules.greeting import greeting
from modules.random_discord_emoji import random_discord_emoji
from jobs.album_check import album_check
from jobs.boost_reward import boost_reward
from jobs.random_photo import random_photo
from jobs.trivia_check import trivia_check
from jobs.fantasy_football_activity import fantasy_football_activity
from commands.age import age
from commands.album import album
from commands.balance import balance
from commands.bank import bank
from commands.blackjack import blackjack
from commands.bless import bless
from commands.bug import bug
from commands.chat import chat
from commands.clear import clear
from commands.coin import coin
from commands.cs import cs
from commands.dice import dice
from commands.double import double
from commands.emote import emote
from commands.feature import feature
from commands.image import image
from commands.kanye import kanye
from commands.kill import kill
from commands.math import math
from commands.nasa import nasa
from commands.pause import pause
from commands.pay import pay
from commands.payout import payout
from commands.photo import photo
from commands.ping import ping
from commands.play import play
from commands.poll import poll
from commands.queue import queue
from commands.random_unicode_emoji import random_unicode_emoji
from commands.restart import restart
from commands.resume import resume
from commands.retirement import retirement
from commands.stock import stock
from commands.stop import stop
from commands.streak import streak
from commands.test import test
from commands.upload import upload
from commands.version import version
from commands.weather import weather
from commands.wheel import wheel


if __name__ == "__main__":

    # Logging Configuration
    logging.basicConfig(
        format="%(asctime)s-[ %(levelname)s ]:    %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
    )
    handle = "LOGGER"
    logger = logging.getLogger(handle)

    # Time the bot starts
    startTime = time.time()

    # Load .env file with API keys and other secrets
    load_dotenv()

    bot = discord.Bot(intents=discord.Intents.all())
    guild = discord.utils.get(bot.guilds, name="MEGACORD")

    # Queue for /play
    queued = []
    played = []
    nest_asyncio.apply()
    SDL = spotdl.Spotdl(
        client_id=str(os.getenv("SPOTIFY_CLIENT")),
        client_secret=str(os.getenv("SPOTIFY_SECRET")),
        headless=True,
        downloader_settings={"output": "./music/{artists} - {title}.{output-ext}"},
        loop=asyncio.get_event_loop(),
    )

    # Timed Events
    @tasks.loop(minutes=random.randint(120, 240))
    async def skill_check_album(bot):
        await album_check(bot, startTime)

    @tasks.loop(minutes=random.randint(120, 240))
    async def skill_check_trivia(bot):
        await trivia_check(bot, startTime)

    @tasks.loop(time=datetime.time.fromisoformat("13:00:00"))
    async def booster_reward(bot):
        await boost_reward(bot, startTime)

    @tasks.loop(time=datetime.time.fromisoformat("13:00:00"))
    async def post_random_photo(bot):
        await random_photo(bot, startTime)

    @tasks.loop(time=datetime.time.fromisoformat("16:00:00"))
    async def post_fantasy_football_activity(bot):
        await fantasy_football_activity(bot, startTime)

    # Event Listeners
    @bot.listen("on_ready")
    async def on_ready():
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="You..."
            ),
        )
        skill_check_album.start(bot)
        skill_check_trivia.start(bot)
        booster_reward.start(bot)
        post_random_photo.start(bot)
        post_fantasy_football_activity.start(bot)

    @bot.listen("on_message")
    async def on_message(message):

        if "testing event listeners..." in message.content.lower():
            await message.edit("\n\n✅ MEGABOT Testing Done!")

        if message.author == bot.user:
            return

        if random.random() < 0.2:
            emoji = await random_discord_emoji(guild, bot, "MEGACORD")
            try:
                await message.add_reaction(emoji)
            except discord.errors.HTTPException:
                pass

        if "birthday" in message.content.lower():
            await message.channel.send("Happy Birthday! 🎈🎉")

        # Random message from greeting.py followed by random emoji
        if bot.user.name.lower() in message.content.lower():
            emoji = await random_discord_emoji(guild, bot, "MEGACORD")
            await message.channel.send(greeting() + "! " + str(emoji))

    @bot.listen("on_member_join")
    async def on_member_join(member):

        guild = discord.utils.get(bot.guilds, name="MEGACORD")
        role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
        await member.add_roles(role)

        channel = discord.utils.get(guild.channels, name="main")
        await channel.send(f"I'm watching you <@{member.id}> 👀...")

    # Slash Commands
    @bot.slash_command(name="age", description="Guesses the age of a specified name.")
    async def call(
        ctx,
        name: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Name to guess age of.",
            required=True,
        ),
    ):
        await age(ctx, name)

    @bot.slash_command(name="album", description="Play an album artist guessing game.")
    async def call(
        ctx,
        genre: discord.Option(
            description="Pick a genre. Hip-Hop is default.",
            default="hip-hop",
            choices=["hip-hop", "pop", "rock", "alternative", "hard-rock"],
        ),
    ):
        await album(ctx, genre)

    @bot.slash_command(name="balance", description="View MEGACOIN balance.")
    async def call(
        ctx,
        user: discord.Option(
            discord.SlashCommandOptionType.user,
            required=False,
            description="User to get the balance of.",
        ),
    ):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**",
                ephemeral=True,
            )
            return
        await balance(ctx, user)

    @bot.slash_command(
        name="bank", description="View the MEGACOIN balance leaderboard."
    )
    async def call(ctx):
        await bank(ctx)

    @bot.slash_command(name="bj", description="Play blackjack.")
    async def call(
        ctx,
        wager: discord.Option(
            discord.SlashCommandOptionType.integer,
            required=True,
            description="Amount you want to wager in blackjack.",
        ),
    ):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**",
                ephemeral=True,
            )
            return
        await blackjack(ctx, wager)

    @bot.slash_command(name="bless", description="Blesses the mess!")
    async def call(ctx):
        await bless(ctx)

    @bot.slash_command(name="bug", description="Report a MEGABOT bug.")
    async def call(
        ctx,
        title: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Give the bug a title.",
        ),
        description: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Describe the bug behavior.",
        ),
    ):
        await bug(ctx, title, description)

    @bot.slash_command(name="chat", description="Chat with MEGABOT.")
    async def call(
        ctx,
        prompt: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Prompt for MEGABOT to respond to.",
            required=True,
        ),
    ):
        await chat(ctx, prompt)

    @bot.slash_command(
        name="clear", description="Temporarily clear MEGATEST commands. (Admin Only)"
    )
    async def call(ctx):
        await clear(ctx)

    @bot.slash_command(name="coin", description="Flip a coin.")
    async def call(ctx):
        await coin(ctx)

    @bot.slash_command(
        name="cs", description="Retrieve a player's Counter-Strike stats."
    )
    async def call(
        ctx,
        username: discord.Option(
            discord.SlashCommandOptionType.string,
            description="User on Steam, a Steam ID, Steam Community URI, or Steam Vanity Username.",
            required=True,
        ),
    ):
        await cs(ctx, username)

    @bot.slash_command(name="dice", description="Roll a dice.")
    async def call(ctx):
        await dice(ctx)

    @bot.slash_command(name="double", description="Play MEGACOIN double or nothing.")
    async def call(
        ctx,
        wager: discord.Option(
            discord.SlashCommandOptionType.integer,
            required=True,
            description="Amount you want to wager.",
        ),
    ):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**",
                ephemeral=True,
            )
            return
        await double(ctx, wager)

    @bot.slash_command(name="emote", description="Search for a 7TV emote.")
    async def call(
        ctx,
        search: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Emote to search for.",
            required=True,
        ),
        add: discord.Option(
            discord.SlashCommandOptionType.boolean,
            description="Add emote to server?",
            required=False,
        ),
    ):
        await emote(ctx, search, add)

    @bot.slash_command(name="feature", description="Submit a MEGABOT feature request.")
    async def call(
        ctx,
        title: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Give the feature request a title.",
        ),
        description: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Describe the feature you desire.",
        ),
    ):
        await feature(ctx, title, description)

    @bot.slash_command(name="image", description="Generate an image with AI.")
    async def call(
        ctx,
        prompt: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Prompt for image to be generated from.",
            required=True,
        ),
    ):
        await image(ctx, prompt)

    @bot.slash_command(name="kanye", description="Retrieve a random Kanye West quote.")
    async def call(ctx):
        await kanye(ctx)

    @bot.slash_command(name="kill", description="Stop MEGABOT. (Admin Only)")
    async def call(ctx):
        await kill(ctx)

    @bot.slash_command(name="math", description="Evaluate provided math expression.")
    async def call(
        ctx,
        expression: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Expression to evaluate.",
            required=True,
        ),
    ):
        await math(ctx, expression)

    @bot.slash_command(name="nasa", description="Retrieve the NASA photo of the day.")
    async def call(
        ctx,
        details: discord.Option(
            discord.SlashCommandOptionType.boolean,
            description="Provide the explanation of the photo.",
            required=False,
        ),
    ):
        await nasa(ctx, details)

    @bot.slash_command(name="pause", description="Pause or resume music.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        await pause(ctx)

    @bot.slash_command(name="pay", description="Pay another user some MEGACOIN.")
    async def call(
        ctx,
        user: discord.Option(
            discord.SlashCommandOptionType.user,
            required=True,
            description="User to pay.",
        ),
        amount: discord.Option(
            discord.SlashCommandOptionType.integer,
            required=True,
            description="Amount to pay.",
        ),
    ):
        await pay(ctx, user, amount)

    @bot.slash_command(name="payout", description="Payout MEGACOIN. (Admin only)")
    async def call(
        ctx,
        user: discord.Option(
            discord.SlashCommandOptionType.user,
            required=True,
            description="User to pay.",
        ),
        amount: discord.Option(
            discord.SlashCommandOptionType.integer,
            required=True,
            description="Amount to pay.",
        ),
        message: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Message to send.",
        ),
    ):
        await payout(ctx, user, amount, message)

    @bot.slash_command(
        name="photo", description="Return a random photo from the MEGABOT database."
    )
    async def call(ctx):
        await photo(ctx)

    @bot.slash_command(name="ping", description="Responds with pong.")
    async def call(ctx):
        await ping(ctx)

    @bot.slash_command(name="play", description="Plays music.")
    async def call(
        ctx,
        search: discord.Option(
            discord.SlashCommandOptionType.string,
            description="YouTube song search or YouTube, TIDAL, Spotify URL.",
            required=True,
        ),
    ):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        await play(ctx, search, queued, played, SDL, skip=False, replay=False)

    @bot.slash_command(
        name="poll", description="Create a poll with up to nine options."
    )
    async def call(
        ctx,
        question: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Question to poll for.",
        ),
        option1: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="First option.",
        ),
        option2: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            description="Second option.",
        ),
        option3: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Third option.",
        ),
        option4: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Fourth option.",
        ),
        option5: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Fifth option.",
        ),
        option6: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Sixth option.",
        ),
        option7: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Seventh option.",
        ),
        option8: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Eigth option.",
        ),
        option9: discord.Option(
            discord.SlashCommandOptionType.string,
            required=False,
            description="Ninth option.",
        ),
    ):
        await poll(
            ctx,
            question,
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            option8,
            option9,
        )

    @bot.slash_command(name="queue", description="Show the current music queue.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        await queue(ctx, queued)

    @bot.slash_command(
        name="random-unicode-emoji",
        description="Return a random Unicode emoji. No Discord emojis.",
    )
    async def call(ctx):
        await random_unicode_emoji(ctx)

    @bot.slash_command(name="restart", description="Restart MEGABOT. (Admin Only)")
    async def call(ctx):
        await restart(ctx)

    @bot.slash_command(
        name="retirement",
        description="Retirement calculator for your planning pleasure.",
    )
    async def call(
        ctx,
        age: discord.Option(
            discord.SlashCommandOptionType.integer,
            description="How old are you?",
            required=True,
        ),
        startingcash: discord.Option(
            discord.SlashCommandOptionType.integer,
            description="Current investments.",
            required=True,
        ),
        yearlysavings: discord.Option(
            discord.SlashCommandOptionType.integer,
            description="Money saved each year.",
            required=True,
        ),
        desiredincome: discord.Option(
            discord.SlashCommandOptionType.integer,
            description="Desired yearly income at retirement.",
            required=True,
        ),
        growthrate: discord.Option(
            discord.SlashCommandOptionType.integer,
            description="Optimistic => %, Expected => %, Conservative => %",
            required=True,
        ),
    ):
        await retirement(
            ctx, age, startingcash, yearlysavings, desiredincome, growthrate
        )

    @bot.slash_command(name="replay", description="Replay the current song.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        search = ""
        await play(ctx, search, queued, played, SDL, skip=False, replay=True)

    @bot.slash_command(name="resume", description="Resume playing music.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        await resume(ctx)

    @bot.slash_command(name="skip", description="Skip the current song.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        search = ""
        await play(ctx, search, queued, played, SDL, skip=True, replay=False)

    @bot.slash_command(name="stock", description="Searches a stock price.")
    async def call(
        ctx,
        symbol: discord.Option(
            discord.SlashCommandOptionType.string,
            description="Stock symbol to search for (ie. PLTR).",
            required=True,
        ),
    ):
        await stock(ctx, symbol)

    @bot.slash_command(name="stop", description="Stops music.")
    async def call(ctx):
        if not (ctx.channel.name == "music" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#956737389454311506>**",
                ephemeral=True,
            )
            return
        await stop(ctx, queued)

    @bot.slash_command(name="streak", description="Keep a daily streak going!")
    async def call(
        ctx,
        stats: discord.Option(
            discord.SlashCommandOptionType.boolean,
            description="Get streak stats.",
            required=False,
        ),
    ):
        if not (ctx.channel.name == "streaks" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1022570321930358895>**",
                ephemeral=True,
            )
            return
        await streak(ctx, stats)

    @bot.slash_command(name="test", description="Test MEGABOT.")
    async def call(ctx):
        await test(ctx, startTime)

    @bot.slash_command(
        name="upload", description="Upload a photo to the MEGABOT database."
    )
    async def call(
        ctx,
        photo: discord.Option(
            discord.SlashCommandOptionType.attachment,
            required=True,
            description="Photo to upload.",
        ),
    ):
        await upload(ctx, photo)

    @bot.slash_command(
        name="version", description="Return the latest MEGABOT version number."
    )
    async def call(ctx):
        await version(ctx)

    @bot.slash_command(name="weather", description="Seven day weather forecast.")
    async def call(
        ctx,
        zipcode: discord.Option(
            discord.SlashCommandOptionType.string,
            required=True,
            descripton="ZIP code for weather.",
        ),
    ):
        view = await weather(ctx, zipcode)
        await ctx.respond(view=view)

    @bot.slash_command(name="wheel", description="Spin the MEGACOIN wheel.")
    async def call(
        ctx,
        wager: discord.Option(
            discord.SlashCommandOptionType.integer,
            required=True,
            description="Amount you want to wager.",
        ),
    ):
        if not (ctx.channel.name == "casino" or ctx.channel.name == "bot-testing"):
            await ctx.send_response(
                content="❗**ERROR: You can only use this command in <#1091083497868886108>**",
                ephemeral=True,
            )
            return
        await wheel(ctx, wager)

    # Start the bot
    bot.run(os.getenv("DISCORD_TOKEN"))
