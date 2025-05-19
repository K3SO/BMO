import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final

# Declara las variables de .env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: Final[str] = os.getenv('PREFIX')
GUILD_ID = discord.Object(id=os.getenv('DEV_GUILD'))

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}!\nPrefijo establecido como: "{PREFIX}"')

client.run(token=TOKEN)