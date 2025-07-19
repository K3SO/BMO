import discord
import leveling
import moderation

def command_log(command):
    print(f'[DEBUG] Se ha usado el comando "{command}"')

# Determina la respuesta que tiene que dar
async def get_response(message: discord.Message, user_message: str, bot, guild_id) -> str:
    user_message = user_message[1:]
    command: str = user_message.lower()

    # Envía una lista con los comandos disponibles
    if command in ('help', 'h', 'ayuda'):
        command_log(command)
        await message.channel.send('Aquí irá un futuro canal con toda la información del bot.')

    # Comandos
    ## Xp
    elif command in ('xp'):
        command_log(command)
        await leveling.get_xp(message, bot)

    ## Moderación
    elif command[:5] in ('warn '):
        command_log(command)
        await moderation.warn(message, command, bot, guild_id)

    # Envia un mensaje avisando que el comando no existe
    else:
        print(f'[DEBUG] Se ha intentado usar un comando desconocido: "{command}"')
        await message.channel.send('Ese comando no extiste... (aún)')