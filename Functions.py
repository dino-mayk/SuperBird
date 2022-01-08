import pygame, os

# load images
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

# load music
def main_music_play():
    pygame.mixer.init()
    pygame.mixer.music.load("data/sounds/main_menu_sound.mp3")
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(loops=-1)

def game_music_play(name):
    pygame.mixer.init()
    pygame.mixer.music.load(f"data/sounds/{name}")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def complete_removal():
    pass