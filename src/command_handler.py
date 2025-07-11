import discord
import leveling

# Determina la respuesta que tiene que dar
async def get_response(message: discord.Message, user_message: str, bot, guild_id) -> str:
    user_message = user_message[1:]
    lowered_message: str = user_message.lower()

    # Envía una lista con los comandos disponibles
    if lowered_message in ('help', 'h', 'ayuda'):
        print(f'[DEBUG] Se ha usado el comando "{lowered_message}"')
        await message.channel.send('Aquí irá un futuro canal con toda la información del bot.')

    # Comandos
    elif lowered_message in ('xp'):
        print(f'[DEBUG] Se ha usado el comando "{lowered_message}"')
        await leveling.get_xp(message, bot)

    # Envia un mensaje avisando que el comando no existe
    else:
        print(f'[DEBUG] Se ha intentado usar un comando desconocido: "{lowered_message}"')
        await message.channel.send('Ese comando no extiste... (aún)')