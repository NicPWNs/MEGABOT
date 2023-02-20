import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')


@client.event
async def on_member_join(member):

    guild = discord.utils.get(client.guilds, name=GUILD)

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

client.run(TOKEN)
