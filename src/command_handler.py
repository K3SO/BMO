import leveling

def command_log(command):
    print(f'[DEBUG] Se ha usado el comando "{command}"')

# Determina la respuesta que tiene que dar
async def get_response(message, user_message, bot):
    user_message = user_message[1:]
    command = user_message.lower()
    command_parts = tuple(command.split())

    # Envía una lista con los comandos disponibles
    if command_parts[0] in ('help', 'h', 'ayuda'):
        command_log(command)
        await message.channel.send('Aquí irá un futuro canal con toda la información del bot.')

    # Comandos
    ## Xp
    elif command_parts[0] in ('xp'):
        command_log(command)
        if len(command_parts) >= 2:
            part = command_parts[1]
            if part[:2] == '<@' and part[-1:] == '>':
                user = await bot.fetch_user(part[2:-1])
            else:
                await message.channel.send('Haz el favor de poner un usuario válido')
                return
        else:
            user = message.author
        
        await leveling.get_xp(user, message.channel)

    # Envia un mensaje avisando que el comando no existe
    else:
        print(f'[DEBUG] Se ha intentado usar un comando desconocido: "{command}"')
        await message.channel.send('Ese comando no extiste... (aún)')