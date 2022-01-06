import random
from Constants import *
from Functions import *


# init
pygame.init()
size = width, height = SIZE_SCREEN
screen = pygame.display.set_mode(size)

# sprites groups
menu_background_sprites = pygame.sprite.Group()
menu_button_sprites = pygame.sprite.Group()
main_sprites = pygame.sprite.Group()
temporary_sprites = pygame.sprite.Group()


class Cursor(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/cursor.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        pygame.mouse.set_visible(False)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, args):
        self.rect.x = args[0]
        self.rect.y = args[1]


class Menu_background_sprite(pygame.sprite.Sprite):
    images = [load_image("sprites/decoration/main/backgrounds/clouds/cloud1.png", color_key=-1),
              load_image("sprites/decoration/main/backgrounds/clouds/cloud2.png", color_key=-1),
              load_image("sprites/decoration/main/backgrounds/clouds/cloud3.png", color_key=-1)]

    def __init__(self, group):
        super().__init__(group)
        self.image = random.choice(Menu_background_sprite.images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + 150)
        self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        if pygame.sprite.spritecollideany(self, menu_background_sprites):
            while pygame.sprite.spritecollideany(self, menu_background_sprites):
                self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + WIDTH_SCREEN * 0.5)
                self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        menu_background_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)

    def update(self):
        if self.rect.x >= -185 and self.rect.y <= 470:
            self.rect.x -= SPEED_TILES_MAIN
        else:
            self.kill()


class Rating_button(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/main/rating.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Rating_button.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 540

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            print('Rating_button')


class Sound_button(pygame.sprite.Sprite):
    image_on = load_image("sprites/decoration/main/sound_on.png", color_key=-1)
    image_off = load_image("sprites/decoration/main/sound_off.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.sound = True
        self.image = Sound_button.image_on
        self.rect = self.image.get_rect()
        self.rect.x = 35
        self.rect.y = 550

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.sound = not self.sound
            if self.sound:
                self.image = Sound_button.image_on
                pygame.mixer.music.set_volume(0.03)
            else:
                self.image = Sound_button.image_off
                pygame.mixer.music.set_volume(0)


class Roll_up_button(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/main/hide.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Roll_up_button.image
        self.rect = self.image.get_rect()
        self.rect.x = 565
        self.rect.y = -10

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pygame.display.iconify()