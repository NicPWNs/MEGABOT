import os
import requests
import discord
from discord import option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


# Application "Slash" Commands
@bot.slash_command(name="ping", description="Responds with pong.", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("Pong! 🏓")


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

    await ctx.respond(f"{response}")


@bot.slash_command(name="math", description="Evaluate provided math expression.", guild_ids=[GUILD_ID])
@option(
    name="expression",
    description="Expression to evaluate.",
    input_type=str,
    required=True
)
async def math(ctx, expression):

    response = str(eval(expression))

    await ctx.respond(f"{response}")


@bot.slash_command(name="bless", description="Blesses the mess!", guild_ids=[GUILD_ID])
async def bless(ctx):
    await ctx.respond("The mess has been blessed! ✨")


@bot.slash_command(name="chat", description="Chat with MEGABOT.", guild_ids=[GUILD_ID])
@option(
    name="prompt",
    description="Prompt for MEGABOT to respond to.",
    input_type=str,
    required=True
)
async def age(ctx, prompt):

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

    r = requests.post("https://api.openai.com/v1/completions",
                      json=params, headers=headers).json()

    response = r["choices"][0]["text"]

    await ctx.respond("*⏳ Loading...*")
    await ctx.send_followup(f"{response}")


@bot.listen
async def on_message(message):

    if 'birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if 'megabot' or '1077260321833635941' in message.content.lower():
        await message.channel.send('Hello there! 👋')


@bot.listen
async def on_member_join(member):

    guild = discord.utils.get(bot.guilds, name=GUILD)

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

    channel = discord.utils.get(guild.channels, name="main")

    await channel.send(f"I'm watching you <@{member.id}>")


bot.run(TOKEN)
