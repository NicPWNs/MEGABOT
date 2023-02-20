import os

import discord
from discord import app_commands
from dotenv import load_dotenv
import interactions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')

intents = discord.Intents.default()
intents.messages = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
guild = discord.utils.get(client.guilds, name=GUILD)
bot = interactions.Client(token=TOKEN)


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

    role = discord.utils.get(guild.roles, name="MEGAENJOYERS")
    await member.add_roles(role)

    channel = discord.utils.get(guild.channels, name="main")

    await channel.send(f"I'm watching you <@{member.id}>")


@bot.command(
    name="test",
    description="This is the first command I made!",
    scope=GUILD_ID,
)
async def test(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")


client.run(TOKEN)
bot.start()
