import os
import requests
import discord
from discord import option
from dotenv import load_dotenv
from slash_commands import ping

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

bot = discord.Bot(intents=discord.Intents.all())


@bot.slash_command(name="ping", description="Responds with pong.", callback=ping, guild_ids=[GUILD_ID])
@bot.slash_command(name="age", description="Guesses the age of a specified name.", guild_ids=[GUILD_ID])
@option(
    name="name",
    description="Name to guess age of.",
    input_type=str,
    required=True
)
async def age(ctx, name):
    r = requests.get('https://api.agify.io/?name=' + name).json()
    age = r["age"]

    if age is None:
        response = "Name not found!"
    else:
        response = f"I guess the age of \"{name}\" is {age}!"

    await ctx.respond(content=f"{response}")


@bot.slash_command(name="math", description="Evaluate provided math expression.", guild_ids=[GUILD_ID])
@option(
    name="expression",
    description="Expression to evaluate.",
    input_type=str,
    required=True
)
async def math(ctx, expression):

    response = str(eval(expression))

    await ctx.respond(content=f"{response}")


@bot.slash_command(name="bless", description="Blesses the mess!", guild_ids=[GUILD_ID])
async def bless(ctx):
    await ctx.respond(content="The mess has been blessed! ✨")


@bot.slash_command(name="chat", description="Chat with MEGABOT.", guild_ids=[GUILD_ID])
@option(
    name="prompt",
    description="Prompt for MEGABOT to respond to.",
    input_type=str,
    required=True
)
async def chat(ctx, prompt):

    params = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 4000,
        'temperature': 1,
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': str(os.getenv('OPENAI_TOKEN')),
    }

    await ctx.respond(content="*⏳ Loading...*")

    r = requests.post("https://api.openai.com/v1/completions",
                      json=params, headers=headers).json()

    response = r["choices"][0]["text"]

    await ctx.edit(content=f"{response}")


@bot.slash_command(name="nasa", description="Retrieve the NASA photo of the day.", guild_ids=[GUILD_ID])
@option(
    name="details",
    description="Provide the explanation of the photo.",
    input_type=discord.SlashCommandOptionType.boolean,
    required=False,
    choices=["True", "False"]
)
async def nasa(ctx, details):
    r = requests.get(
        'https://api.nasa.gov/planetary/apod?api_key=' + str(os.getenv('NASA_KEY'))).json()

    desc = ""

    if details == "True":
        desc = r["explanation"]

    response = r["url"] + "\n" + desc

    await ctx.respond(content=f"{response}")


@bot.slash_command(name="kanye", description="Retrieve a random Kanye West quote.", guild_ids=[GUILD_ID])
async def kanye(ctx):
    r = requests.get('https://api.kanye.rest/').json()

    quote = r["quote"]
    response = f"<:kanye:1078059327891439657>💬  ❝ {quote} ❞"

    await ctx.respond(content=f"{response}")


@bot.slash_command(name="csgo", description="Retrieve CS:GO stats.", guild_ids=[GUILD_ID])
@option(
    name="username",
    description="User on Steam, a Steam ID, Steam Community URI, or Steam Vanity Username.",
    input_type=discord.SlashCommandOptionType.string,
    required=True
)
async def csgo(ctx, username):

    headers = {
        "TRN-Api-Key": os.getenv('TRN_KEY'),
    }

    await ctx.respond(content="*⏳ Loading...*")

    r = requests.get(
        'https://public-api.tracker.gg/v2/csgo/standard/profile/steam/' + username, headers=headers).json()

    handle = r["data"]["platformInfo"]["platformUserHandle"]

    types = [
        "timePlayed",
        "score",
        "kills",
        "deaths",
        "kd",
        "damage",
        "headshots",
        "shotsFired",
        "shotsHit",
        "shotsAccuracy",
        "snipersKilled",
        "bombsPlanted",
        "bombsDefused",
        "moneyEarned",
        "hostagesRescued",
        "mvp",
        "wins",
        "ties",
        "matchesPlayed",
        "losses",
        "roundsPlayed",
        "roundsWon",
        "wlPercentage",
        "headshotPct",
    ]

    stat = f"__**{handle} Stats:**__\n"

    for i in range(0, len(types)):
        stat += "**" + \
            str(r["data"]["segments"][0]["stats"]
                [types[i]]["displayName"]) + ":**  " + \
            str(r["data"]["segments"][0]["stats"]
                [types[i]]["displayValue"]) + "\n"

    await ctx.edit(content=f"{stat}")


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


bot.run(TOKEN)
