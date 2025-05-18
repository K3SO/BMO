import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final

# Declara las variables de .env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: Final[str] = os.getenv('PREFIX')
DEV_GUILD: Final[int] = os.getenv('DEV_GUILD')

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)
GUILD_ID = discord.Object(id=DEV_GUILD)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}!\nPrefijo establecido como: "{PREFIX}"')
    try:
        guild = discord.Object(id=DEV_GUILD)
        synced = await client.tree.sync(guild=guild)
        print(f'Se han sincronizado {len(synced)} salsh commands')
    except Exception as e:
        print(f'[ERROR] No se han podido sincronizar los comandos: {e}')

@client.tree.command(name='test1', description='hace un test', guild=GUILD_ID)
async def caca(interaction: discord.Interaction):
    await interaction.response.send_message('una prueba')

@client.command(name='test2', aliases=['t2'])
async def pis(ctx):
    await ctx.send('dos prueba')

client.run(token=TOKEN)