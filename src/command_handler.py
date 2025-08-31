import discord
import leveling

def command_log(command):
    print(f'[DEBUG] Se ha usado el comando "{command}"')

# Determina la respuesta que tiene que dar
async def get_response(message, user_message, bot):
    user_message = user_message[1:]
    command = user_message.lower()

    # Envía una lista con los comandos disponibles
    if command in ('help', 'h', 'ayuda'):
        command_log(command)
        await message.channel.send('Aquí irá un futuro canal con toda la información del bot.')

    # Comandos
    ## Xp
    elif command in ('xp'):
        command_log(command)
        await leveling.get_xp(message.author, message.channel)

    # Envia un mensaje avisando que el comando no existe
    else:
        print(f'[DEBUG] Se ha intentado usar un comando desconocido: "{command}"')
        await message.channel.send('Ese comando no extiste... (aún)')