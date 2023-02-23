from dotenv import load_dotenv
from discord import option
import discord
import os
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "/slash_commands/*.py"))
ignore = ['__init__.py', 'megabot.py']
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith(ignore)]


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
