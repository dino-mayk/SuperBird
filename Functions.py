import os, sqlite3, pygame


def login_check(login):
    if len(login) < 5 or len(login) > 20:
        return False
    return True


def password_check(password):
    if len(password) < 8 or len(password) > 20:
        return False
    return True


def background_music_play():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sounds/background.mp3'), loops=-1)
    pygame.mixer.Channel(0).set_volume(0.01)


def game_music_play(name):
    pygame.mixer.init()
    pygame.mixer.music.load(f"data/sounds/{name}")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play()


def load_image(name, color_key=False):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def update_gold(user_id, gold_count):
    con = sqlite3.connect('data/Database.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE Users SET gold = (SELECT gold FROM Users WHERE 
        id = {user_id}) + {gold_count} WHERE id = {user_id}""")
    con.commit()
    con.close()