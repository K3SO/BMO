import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import command_handler
import utility
from leveling import recover_roles, xp

# Declara las variables de .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
GUILD_ID = int(os.getenv('DEV_GUILD'))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

utility.db_execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_name STRING,
    user_xp INTEGER DEFAULT 0,
    user_lvl INTEGER DEFAULT 0
)
''')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!\nPrefijo establecido como: "{PREFIX}"')

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(GUILD_ID)
    await recover_roles(member, guild)
    print(f'[DEBUG] {member.name} se ha unido al servidor')

@bot.event
async def on_message(message: discord.Message):
    guild = bot.get_guild(GUILD_ID)
    if not message.content or message.author.bot:
        return
    
    # Acceso a los comandos
    if message.content[0] == PREFIX:
        await command_handler.get_response(message, message.content, bot)

    # Xp
    else:
        await xp(message, message.author, guild)

bot.run(token=TOKEN)