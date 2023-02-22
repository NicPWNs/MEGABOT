import os
import requests
import discord
from discord import option
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

client = discord.Bot()


# Application "Slash" Commands
@client.slash_command(name="ping", description="Responds with pong.", guild_ids=[GUILD_ID])
async def ping(ctx):
    await ctx.respond("Pong! 🏓")


@client.slash_command(name="age", description="Guesses the age of a specified name.", guild_ids=[GUILD_ID])
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
        response = f"I guess the name of {name} is {age}!"

    await ctx.respond(f"{response}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if 'birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if 'megabot' in message.content.lower():
        await message.channel.send('Hello there! 👋')


@client.event
async def on_member_join(member):

    guild = discord.utils.get(client.guilds, name=GUILD)

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

    channel = discord.utils.get(guild.channels, name="main")

    await channel.send(f"I'm watching you <@{member.id}>")


client.run(TOKEN)
