import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)


# Application "Slash" Commands
@tree.command(name='ping', description='Responds with pong.', guild=discord.Object(id=GUILD_ID))
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! 🏓")


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


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))


client.run(TOKEN)
