import discord
import sqlite3

def lvl_function(user_lvl) -> int:
    lvl_base = 100
    return lvl_base * (user_lvl + 1)

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
    message_xp = round(5 + message_xp ** 0.9)
    user_xp += message_xp

    # Determinar si el usuario tiene la experiencia suficente para subir de nivel
    xp_goal = lvl_function(user_lvl)
    get_role_calls = []
    if user_xp >= xp_goal:
        while user_xp >= xp_goal:
            user_lvl += 1
            user_xp -= xp_goal
            xp_goal = lvl_function(user_lvl)
            get_role_calls.append(user_lvl)
        await message.channel.send(f'{message.author.mention}, has subido al nivel {user_lvl}!') # Cambiar mensaje?

    # Actualizar los datos en la base de datos
    cursor.execute('UPDATE users SET user_xp = ?, user_lvl = ? WHERE user_id = ?', (user_xp, user_lvl, user_id))

    connection.commit()
    connection.close()

    for call in get_role_calls:
        await get_role(call, message, bot, guild_id)

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
    member = message.author

    # Diccionario con los roles de nivel (dependiendo del nivel)
    level_roles = {
        1:1378504557864419359,
        5:1378504698549506272,
        10:1378505641555132529,
        15:1378505829841637516,
        20:1378506218485579916,
        25:1378505478816137348,
        30:1378506407485374675,
        35:1378506510757396562,
        40:1378506612259684482,
        45:1378506652248047738,
        50:1378506709869264997,
    }

    # Añade el rol de nivel (dependiendo del nivel)
    role_id = level_roles.get(lvl)
    if role_id:
        role = guild.get_role(role_id)
        if role not in member.roles:
            await member.add_roles(role)
            # Quita los roles de nivel que no corresponden
            for level, role_id in level_roles.items():
                if level != lvl:
                    role = guild.get_role(role_id)
                    if role in member.roles:
                        await member.remove_roles(role)

    # Diccionario con los roles de estatus (dependiendo del nivel)
    status_roles = {
        0:1378507600471265290, # colega
        5:1378507735913730088, # sociable
        25:1378513324970344488, # bocachancla
    }

    # Añade el rol de estatus (dependiendo del nivel)
    role_id = status_roles.get(lvl)
    if role_id:
        role = guild.get_role(role_id)
        if role not in member.roles:
            await member.add_roles(role)
            # Quita los roles de estatus que no corresponden
            for level, role_id in status_roles.items():
                if level != lvl:
                    role = guild.get_role(role_id)
                    if role in member.roles:
                        await member.remove_roles(role)