import discord
import sqlite3

def lvl_function(user_lvl) -> int:
    lvl_base = 100
    # fórmula 1: lineal
    xp = lvl_base * (user_lvl + 1)
    return xp

async def xp(message, bot, guild_id):
    connection = sqlite3.connect('bmo_data.db')
    cursor = connection.cursor()

    user_id = message.author.id

    # Insertar la ID del usuario si no existe el usuario en la base de datos
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id) VALUES (?)
    ''', (user_id,))

    # Sacar la información del usuario de la base de datos
    cursor.execute('SELECT user_xp, user_lvl FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone() # Tupla
    user_xp = user_data[0]
    user_lvl = user_data[1]

    # Sumar la experiencia obtenida con el mensaje
    message_xp = len(message.content)
    user_xp += message_xp

    # Determinar si el usuario tiene la experiencia suficente para subir de nivel
    xp_goal = lvl_function(user_lvl)
    if user_xp >= xp_goal:
        while user_xp >= xp_goal:
            user_lvl += 1
            user_xp -= xp_goal
            xp_goal = lvl_function(user_lvl)
            await get_role(user_lvl, message, bot, guild_id)
        await message.channel.send(f'{message.author.mention}, has subido al nivel {user_lvl}!') # Cambiar mensaje?

    # Actualizar los datos en la base de datos
    cursor.execute('UPDATE users SET user_xp = ?, user_lvl = ? WHERE user_id = ?', (user_xp, user_lvl, user_id))

    connection.commit()
    connection.close()

async def get_xp(message, bot):
    connection = sqlite3.connect('bmo_data.db')
    cursor = connection.cursor()

    user_id = message.author.id

    # Insertar la ID del usuario si no existe el usuario en la base de datos
    cursor.execute('''
    INSERT OR IGNORE INTO users (user_id) VALUES (?)
    ''', (user_id,))

    # Sacar la información del usuario de la base de datos
    cursor.execute('SELECT user_xp, user_lvl FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone() # Tupla
    user_xp = user_data[0]
    user_lvl = user_data[1]
    user_name = await bot.fetch_user(user_id)
    xp_goal = lvl_function(user_lvl)

    user_icon = message.author.avatar.url
    bar_length = 10
    filled_length = int(bar_length * user_xp // xp_goal)
    bar = "█" * filled_length + "─" * (bar_length - filled_length)

    # Crear el embed
    embed = discord.Embed(
        color=discord.Color.teal()
    )
    # embed.set_author(name=f'{user_name}', icon_url=user_icon)
    embed.set_thumbnail(url=user_icon)
    embed.add_field(name=f'Nivel - **{user_lvl}**', value=f'**{user_xp} / {xp_goal}**\n\n{bar}')

    # Enviar el embed
    await message.channel.send(embed=embed)

    connection.commit()
    connection.close()

async def get_role(lvl, message, bot, guild_id):
    guild = bot.get_guild(guild_id)