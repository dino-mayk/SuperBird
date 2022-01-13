import pygame, os


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


def game_music_play(name):
    pygame.mixer.init()
    pygame.mixer.music.load(f"data/sounds/{name}")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play()


def login_check(login):
    if len(login) < 3 or len(login) > 20:
        return False
    return True


def password_check(password):
    if len(password) < 5 or len(password) > 20:
        return False
    return True