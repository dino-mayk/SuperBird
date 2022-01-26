from Functions import *
from Constants import *
import random


# init
pygame.init()
screen = pygame.display.set_mode(DEFAULT_SIZE_SCREEN)


# sprites groups
main_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
menu_button_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()
ticket_sprites = pygame.sprite.Group()
temporary_sprites = pygame.sprite.Group()


# sprite functions
def full_cleaning_sprites():
    background_sprites.empty()
    menu_button_sprites.empty()
    player_sprite.empty()
    pipe_sprites.empty()
    ticket_sprites.empty()
    temporary_sprites.empty()


# additional variables
speed_pipes = 2
count_tickets = 0
score = 0
gravity = INITIAL_GRAVITY


# sound
sound = 1
pygame.mixer.set_num_channels(3)
pygame.mixer.Channel(1).set_volume(0.1)


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
    def __init__(self, group, name):
        super().__init__(group)
        self.images = [load_image(f"sprites/backgrounds/{name}/1.png", color_key=-1),
                  load_image(f"sprites/backgrounds/{name}/2.png", color_key=-1),
                  load_image(f"sprites/backgrounds/{name}/3.png", color_key=-1)]
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(DEFAULT_WIDTH_SCREEN, DEFAULT_WIDTH_SCREEN + 150)
        self.rect.y = random.randrange(50, DEFAULT_HEIGHT_SCREEN - 80)
        if pygame.sprite.spritecollideany(self, background_sprites):
            while pygame.sprite.spritecollideany(self, background_sprites):
                self.rect.x = random.randrange(DEFAULT_WIDTH_SCREEN, DEFAULT_WIDTH_SCREEN + DEFAULT_WIDTH_SCREEN * 0.5)
                self.rect.y = random.randrange(50, DEFAULT_HEIGHT_SCREEN - 80)
        background_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)

    def update(self):
        if self.rect.x >= -185 and self.rect.y <= 470:
            self.rect.x -= SPEED_TILES_BACKGROUND
        else:
            self.kill()


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
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(player_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect.x = PLAYER_COORD_X
        self.rect.y = DEFAULT_HEIGHT_SCREEN * 0.5

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
        # only for Game
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.rect.y += gravity
        pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= JUMP
            self.image = self.frames[self.cur_frame]
            if sound == 1:
                game_music_play("wing.wav")
        else:
            self.image = self.frames[0]
        if self.rect.y >= DEFAULT_HEIGHT_SCREEN or self.rect.y <= -50 \
                or pygame.sprite.spritecollideany(self, pipe_sprites):
            if sound == 1:
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/sounds/death.wav'))
                pygame.mixer.Channel(2).set_volume(0.1)
            global speed_pipes
            global count_passed_steam_pipes
            speed_pipes = 2
            count_passed_steam_pipes = 0
            self.kill()


class Top_pipe(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/game/top_pipe.png")

    def __init__(self, group):
        super().__init__(group)
        # variable loading
        global coord_top_pipe_sprite
        global y_ticket
        global x_ticket
        # location and picture
        self.image = Top_pipe.image
        self.rect = self.image.get_rect()
        coord_top_pipe_sprite = random.randrange(MIN_POS_TOP_PIPE, MAX_POS_TOP_PIPE)
        self.rect.y = coord_top_pipe_sprite
        self.rect.x = DEFAULT_WIDTH_SCREEN
        if pygame.sprite.spritecollideany(self, pipe_sprites):
            while pygame.sprite.spritecollideany(self, pipe_sprites):
                self.rect.x += SPACE
        # clearing memory and defining a group of sprites
        pipe_sprites.add(self)
        pygame.sprite.Sprite.remove(self, group)
        # ticket actions
        ticket_drop_chance = random.randrange(1, TICKET_DROP_CHANCE + 1)
        if ticket_drop_chance == TICKET_DROP_CHANCE:
            y_ticket = coord_top_pipe_sprite + LEN_PIPES
            x_ticket = self.rect.x
            Ticket(ticket_sprites)
        # check score
        self.passed = False

    def update(self):
        # variable loading
        global speed_pipes
        global gravity
        global count_passed_steam_pipes
        global score
        # action processing
        if self.rect.x <= 150 and self.passed is False:
            score += 1
            self.passed = True
        if self.rect.x > -60:
            self.rect.x -= speed_pipes
        else:
            if score % SPEED_INCREASE_FREQUENCY == 0:
                speed_pipes += RATE_INCREASE_SPEED_PIPE
                gravity += RATE_INCREASE_gravity
            self.kill()


class Bottom_pipe(pygame.sprite.Sprite):
    image = load_image("sprites/decoration/game/bottom_pipe.png", color_key=-1)

    def __init__(self, group):
        super().__init__(group)
        self.image = Bottom_pipe.image
        self.rect = self.image.get_rect()
        self.rect.y = coord_top_pipe_sprite + LEN_PIPES + GAP
        self.rect.x = DEFAULT_WIDTH_SCREEN
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
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/sounds/ticket.wav'))
            global count_tickets
            count_tickets += 1
            self.kill()