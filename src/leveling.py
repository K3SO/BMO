import discord
import utility

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

# Diccionario con los roles de estatus (dependiendo del nivel)
status_roles = {
    0:1378507600471265290, # colega
    5:1378507735913730088, # sociable
    25:1378513324970344488, # bocachancla
}

def lvl_function(user_lvl) -> int:
    lvl_base = 100
    return lvl_base * (user_lvl + 1)

async def xp(message, user, guild):
    utility.ensure_user_exists(user.id, str(user))
    user_data = utility.db_execute('SELECT user_xp, user_lvl FROM users WHERE user_id = ?', (user.id,), fetchone=True)
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
    
    utility.db_execute('UPDATE users SET user_xp = ?, user_lvl = ? WHERE user_id = ?', (user_xp, user_lvl, user.id))

    for call in get_role_calls:
        await get_role(call, user, guild)

async def get_xp(user, channel):
    utility.ensure_user_exists(user.id, str(user))
    user_data = utility.db_execute('SELECT user_xp, user_lvl FROM users WHERE user_id = ?', (user.id,), fetchone=True)
    user_xp = user_data[0]
    user_lvl = user_data[1]

    xp_goal = lvl_function(user_lvl)
    user_icon = user.avatar.url
    bar_length = 10
    filled_length = int(bar_length * user_xp // xp_goal)
    bar = "█" * filled_length + "─" * (bar_length - filled_length)

    embed = discord.Embed(
        color=discord.Color.teal()
    )
    embed.set_thumbnail(url=user_icon)
    embed.add_field(name=f'Nivel - **{user_lvl}**', value=f'**{user_xp} / {xp_goal}**\n\n{bar}')

    await channel.send(embed=embed)

async def get_role(lvl, user, guild):
    role_lists = (level_roles, status_roles)
    for role_list in role_lists:
        # Añade
        role_id = role_list.get(lvl)
        if role_id:
            role = guild.get_role(role_id)
            if role not in user.roles:
                await user.add_roles(role)
                # Quita
                for level, role_id in role_list.items():
                    if level != lvl:
                        role = guild.get_role(role_id)
                        if role in user.roles:
                            await user.remove_roles(role)

async def recover_roles(user, guild):
    utility.ensure_user_exists(user.id, str(user))
    user_data = utility.db_execute('SELECT user_lvl FROM users WHERE user_id = ?', (user.id,), fetchone=True)
    user_lvl = user_data[0]
    get_role_calls = []
    for n in range(user_lvl + 1):
        get_role_calls.append(n)

    for call in get_role_calls:
        await get_role(call, user, guild)