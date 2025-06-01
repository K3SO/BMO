import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from typing import Final
import sqlite3

import command_handler
import message_handler

# Declara las variables de .env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: Final[str] = os.getenv('PREFIX')
GUILD_ID = discord.Object(id=os.getenv('DEV_GUILD'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Crear/conectar la base de datos
connection = sqlite3.connect('bmo_data.db')
cursor = connection.cursor()
# Crear la tabla de los usuarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    user_xp INTEGER DEFAULT 0,
    user_lvl INTEGER DEFAULT 0
)
''')
connection.commit()
connection.close()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}!\nPrefijo establecido como: "{PREFIX}"')

@bot.event
async def on_message(message: discord.Message):
    if not message.content or message.author.bot:
        return
    # print(f'{message.author} ha mandado "{message.content}"')
    if message.content[0] == PREFIX:
        await command_handler.get_response(message, message.content, bot)
    else:
        await message_handler.send(message, bot)

bot.run(token=TOKEN)