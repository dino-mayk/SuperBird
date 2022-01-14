import random
from Constants import *
from Functions import *


# init
pygame.init()
size = width, height = SIZE_SCREEN
screen = pygame.display.set_mode(size)

# sprites groups
main_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
menu_button_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()
ticket_sprites = pygame.sprite.Group()
temporary_sprites = pygame.sprite.Group()

# additional variables
speed_pipes = 2
count_tickets = 0
selected_bird = 'classic'
selected_background = 'clouds'
score = 0

# sound
pygame.mixer.set_num_channels(2)
pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/sounds/main_menu_sound.mp3'), loops=-1)
pygame.mixer.Channel(0).set_volume(0.01)


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


class Background_sprite(pygame.sprite.Sprite):
    images = [load_image(f"sprites/decoration/backgrounds/{selected_background}/1.png", color_key=-1),
              load_image(f"sprites/decoration/backgrounds/{selected_background}/2.png", color_key=-1),
              load_image(f"sprites/decoration/backgrounds/{selected_background}/3.png", color_key=-1)]

    def __init__(self, group):
        super().__init__(group)
        self.image = random.choice(Background_sprite.images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + 150)
        self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        if pygame.sprite.spritecollideany(self, background_sprites):
            while pygame.sprite.spritecollideany(self, background_sprites):
                self.rect.x = random.randrange(WIDTH_SCREEN, WIDTH_SCREEN + WIDTH_SCREEN * 0.5)
                self.rect.y = random.randrange(50, HEIGHT_SCREEN - 80)
        background_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)

    def update(self):
        if self.rect.x >= -185 and self.rect.y <= 470:
            self.rect.x -= SPEED_TILES_BACKGROUND
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
                pygame.mixer.music.set_volume(VOLUME_SOUNDS_MENU)
            else:
                self.image = Sound_button.image_off
                pygame.mixer.Channel(0).set_volume(0)


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


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, menu_image=False):
        super().__init__(player_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        if menu_image is False:
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)
            self.rect.x = PLAYER_COORD_X
            self.rect.y = HEIGHT_SCREEN * 0.5
        else:
            self.image = self.frames[0]
            self.rect = self.rect.move(x, y)
            self.rect.x = 50
            self.rect.y = 100

    def cut_sheet(self, sheet, columns, rows):
        # only for Game
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.rect.y += GRAVITY
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= JUMP
            self.image = self.frames[self.cur_frame]
            game_music_play("wing.wav")
        else:
            self.image = self.frames[0]
        if self.rect.y >= HEIGHT_SCREEN or self.rect.y <= -50 \
                or pygame.sprite.spritecollideany(self, pipe_sprites):
            game_music_play("die.wav")
            global speed_pipes
            global count_passed_steam_pipes
            speed_pipes = 2
            count_passed_steam_pipes = 0
            self.kill()


class Top_pipe(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/game/top_pipe.png")

    def __init__(self, group):
        super().__init__(group)
        global coord_top_pipe_sprite
        global y_ticket
        global x_ticket
        self.image = Top_pipe.image
        self.rect = self.image.get_rect()
        coord_top_pipe_sprite = random.randrange(MIN_POS_TOP_PIPE, MAX_POS_TOP_PIPE)
        self.rect.y = coord_top_pipe_sprite
        self.rect.x = WIDTH_SCREEN
        if pygame.sprite.spritecollideany(self, pipe_sprites):
            while pygame.sprite.spritecollideany(self, pipe_sprites):
                self.rect.x += SPACE
        pipe_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)
        ticket_drop_chance = random.randrange(1, TICKET_DROP_CHANCE + 1)
        if ticket_drop_chance == TICKET_DROP_CHANCE:
            y_ticket = coord_top_pipe_sprite + LEN_PIPES
            x_ticket = self.rect.x
            Ticket(ticket_sprites)

    def update(self):
        global speed_pipes
        global count_passed_steam_pipes
        global score
        if self.rect.x == PLAYER_COORD_X:
            score += 1
        if self.rect.x > -60:
            self.rect.x -= speed_pipes
        else:
            if score % SPEED_INCREASE_FREQUENCY == 0:
                speed_pipes += RATE_INCREASE_SPEED_PIPE
            self.kill()


class Bottom_pipe(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/game/bottom_pipe.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bottom_pipe.image
        self.rect = self.image.get_rect()
        self.rect.y = coord_top_pipe_sprite + LEN_PIPES + GAP
        self.rect.x = WIDTH_SCREEN
        if pygame.sprite.spritecollideany(self, pipe_sprites):
            while pygame.sprite.spritecollideany(self, pipe_sprites):
                self.rect.x += SPACE
        pipe_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)

    def update(self):
        if self.rect.x > -60:
            self.rect.x -= speed_pipes
        else:
            self.kill()


class Ticket(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/game/ticket.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Ticket.image
        self.rect = self.image.get_rect()
        self.rect.x = x_ticket
        self.rect.y = y_ticket

    def update(self):
        self.rect.x -= speed_pipes
        if pygame.sprite.spritecollideany(self, player_sprite):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sounds/point.wav'))
            pygame.mixer.Channel(1).set_volume(0.1)
            global count_tickets
            count_tickets += 1
            self.kill()