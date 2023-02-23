import os
import discord
from discord import option
from dotenv import load_dotenv
from slash_commands.ping import ping
from slash_commands.age import age
from slash_commands.math import math
from slash_commands.bless import bless
from slash_commands.chat import chat
from slash_commands.nasa import nasa
from slash_commands.kanye import kanye
from slash_commands.csgo import csgo
from slash_commands.streak import streak

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

bot = discord.Bot(intents=discord.Intents.all())


@bot.listen('on_message')
async def on_message(message):

    if message.author == bot.user:
        return

    if 'birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if 'megabot' in message.content.lower():
        await message.channel.send('Hello there! 👋')


@bot.listen('on_member_join')
async def on_member_join(member):

    guild = discord.utils.get(bot.guilds, name=GUILD)

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

    channel = discord.utils.get(guild.channels, name="main")

    await channel.send(f"I'm watching you <@{member.id}>")


@bot.slash_command(name="ping", description="Responds with pong.", guild_ids=[GUILD_ID])
async def call(ctx):
    await ping(ctx)


@bot.slash_command(name="age", description="Guesses the age of a specified name.", guild_ids=[GUILD_ID])
@option(
    name="name",
    description="Name to guess age of.",
    input_type=str,
    required=True
)
async def call(ctx, name):
    await age(ctx, name)


@bot.slash_command(name="math", description="Evaluate provided math expression.", guild_ids=[GUILD_ID])
@option(
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
@option(
    name="prompt",
    description="Prompt for MEGABOT to respond to.",
    input_type=str,
    required=True
)
async def call(ctx, prompt):
    await chat(ctx, prompt)


@bot.slash_command(name="nasa", description="Retrieve the NASA photo of the day.", guild_ids=[GUILD_ID])
@option(
    name="details",
    description="Provide the explanation of the photo.",
    input_type=discord.SlashCommandOptionType.boolean,
    required=False,
    choices=["True", "False"]
)
async def call(ctx, details):
    await nasa(ctx, details)


@bot.slash_command(name="kanye", description="Retrieve a random Kanye West quote.", guild_ids=[GUILD_ID])
async def call(ctx):
    await kanye(ctx)


@bot.slash_command(name="csgo", description="Retrieve CS:GO stats.", guild_ids=[GUILD_ID])
@option(
    name="username",
    description="User on Steam, a Steam ID, Steam Community URI, or Steam Vanity Username.",
    input_type=discord.SlashCommandOptionType.string,
    required=True
)
async def call(ctx, username):
    await csgo(ctx, username)


@bot.slash_command(name="streak", description="Keep a daily streak going!", guild_ids=[GUILD_ID])
@option(
    name="stats",
    description="Get streak stats.",
    input_type=discord.SlashCommandOptionType.boolean,
    required=False,
    choices=["True", "False"]
)
async def call(ctx, stats):
    await streak(ctx, stats)


bot.run(TOKEN)
