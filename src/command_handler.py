from discord import Message

# Determina la respuesta que tiene que dar
async def get_response(message: Message, user_message: str) -> str:
    user_message = user_message[1:]
    lowered_message: str = user_message.lower()

    # Envía una lista con los comandos disponibles
    if lowered_message == 'help' or lowered_message == 'h' or lowered_message == 'ayuda':
        print(f'[DEBUG] Se ha usado el comando "{lowered_message}"')
        await message.channel.send('Aquí irá un futuro canal con toda la información del bot.')

    # Comandos
    elif lowered_message == 'play' or lowered_message == 'p':
        print(f'[DEBUG] Se ha usado el comando "{lowered_message}"')
        await message.channel.send('Ese comando está en mantenimiento')

    # Envia un mensaje avisando que el comando no existe
    else:
        print(f'[DEBUG] Se ha intentado usar un comando desconocido: "{lowered_message}"')
        await message.channel.send('Ese comando no extiste... (aún)')