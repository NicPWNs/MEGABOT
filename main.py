import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

guild = discord.utils.get(client.guilds, name=GUILD)


@client.event
async def on_ready():

    print(
        f'{client.user} is connected to:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')


@client.event
async def on_member_join(member):

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

client.run(TOKEN)
