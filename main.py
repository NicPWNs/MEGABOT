import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.utils.get(client.guilds, name=GUILD)


@tree.command(name="test", description="My first application Command", guild=guild)
async def first_command(interaction):
    await interaction.response.send_message("Test!")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if 'happy birthday' in message.content.lower():
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


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    await tree.sync(guild=guild)

client.run(TOKEN)
