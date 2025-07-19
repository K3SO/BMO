import discord
import sqlite3

async def warn(message, command, bot, guild_id):
    if not message.author.guild_permissions.administrator:
        await message.channel.send('Necesitas ser administrador para usar ese comando.')
        return
    user_ping = command[5:]
    user_id = user_ping[2:-1]
    guild = bot.get_guild(guild_id)
    if not guild.get_member(user_id):
        await message.channel.send('Ese usuario no existe.')
        return
    
    connection = sqlite3.connect('bmo_data.db')
    cursor = connection.cursor()

    # Insertar la ID del usuario si no existe el usuario en la base de datos
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id) VALUES (?)
    ''', (user_id,))

    cursor.execute('SELECT warns FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone() # Tupla
    warns = user_data[0]
    
    # Acción principal
    warns += 1

    cursor.execute('UPDATE users SET warns = ? WHERE user_id = ?', (warns, user_id))

    connection.commit()
    connection.close()

    rules_channel = '<#1378475161287659550>'
    await message.channel.send(f'{user_ping}, se te ha añadido un aviso, hasta ahora tienes {warns} avisos.\nRevisa {rules_channel} para no romper ninguna regla y que no te penalicen en un futuro ;)')