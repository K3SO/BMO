from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from command_handler import get_response

# Declara las variables de .env
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
PREFIX: Final[str] = os.getenv('CMMND_PREFIX')

# Saca las dependencias necesarias
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Avisa por la consola que se ha conectado correctamente
@client.event
async def on_ready() -> None:
    print(f'Bot conectado como {client.user}!\nPrefijo establecido como: "{PREFIX}"')

# Detecta los mensajes y filtra los comandos
@client.event
async def on_message(message: Message) -> None:
    if not message.content or message.author.bot:
        return
    if message.content[0] == PREFIX:
        await get_response(message, message.content)

# Inicia el bot con el token en .env
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()