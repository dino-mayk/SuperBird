import random
from Constants import *
from Functions import *


# init
pygame.init()
size = width, height = SIZE_SCREEN
screen = pygame.display.set_mode(size)

# sprites groups
menu_sprites = pygame.sprite.Group()
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


class Tile_menu_background(pygame.sprite.Sprite):
    tiles = [load_image("sprites/decoration/main/backgrounds/clouds/cloud1.png", color_key=-1),
              load_image("sprites/decoration/main/backgrounds/clouds/cloud2.png", color_key=-1),
              load_image("sprites/decoration/main/backgrounds/clouds/cloud3.png", color_key=-1)]

    def __init__(self, group):
        super().__init__(group)
        self.image = random.choice(Tile_menu_background.tiles)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + 150)
        self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        if pygame.sprite.spritecollideany(self, menu_sprites):
            while pygame.sprite.spritecollideany(self, menu_sprites):
                self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + WIDTH_SCREEN * 0.5)
                self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        menu_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)

    def update(self, *args):
        if self.rect.x >= -100:
            self.rect.x -= SPEED_TILES_MAIN
        else:
            pygame.sprite.Sprite.remove(self, menu_sprites)


