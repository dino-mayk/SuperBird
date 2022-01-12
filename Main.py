import sys, pygame_gui, sqlite3
from Sprites import *


def full_cleaning_sprites():
    background_sprites.empty()
    menu_button_sprites.empty()
    player_sprite.empty()
    pipe_sprites.empty()
    ticket_sprites.empty()
    temporary_sprites.empty()


class Entrance:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.language_selection()
        self.InitUI()
        self.loading_data()
        self.running = True

    def language_selection(self):
        if language == 'english':
            self.login = 'To come in'
            self.registration = 'Register'
            self.text_exit = 'Exit'
            self.question = 'Are you sure you want to log out?'
        else:
            self.login = 'Войти'
            self.registration = 'Зарегистрироваться'
            self.text_exit = 'Выйти'
            self.question = 'Вы уверены, что хотите выйти?'

    def InitUI(self):
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 230), (300, 60)),
            text=self.login,
            manager=self.manager,
        )
        self.registration_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 310), (300, 60)),
            text=self.registration,
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 390), (300, 60)),
            text=self.text_exit,
            manager=self.manager
        )

    def show_confirmation_dialog(self):
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((100, 150), (300, 200)),
            manager=self.manager,
            window_title='Exit',
            action_long_desc=self.question,
            action_short_name='Yes',
            blocking=True
        )

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.version = load_image('sprites/decoration/main/version.png', color_key=-1)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def transition(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        Login().run()
                    if event.ui_element == self.registration_button:
                        Registration().run()
                    if event.ui_element == self.exit_button:
                        self.show_confirmation_dialog()
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    self.transition()
                    sys.exit()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Login:
    def __init__(self):
        self.size = self.width, self.height = LOGIN_AND_REGISTRATION_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.language_selection()
        self.InitUI()
        self.loading_data()
        self.running = True

    def language_selection(self):
        if language == 'english':
            self.login = 'To come in'
            self.text_password = 'Password:'
            self.text_nickname = 'Nickname:'
        else:
            self.login = 'Войти'
            self.text_password = 'Пароль:'
            self.text_nickname = 'Прозвище:'

    def InitUI(self):
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 180), (350, 60)),
            text=self.login,
            manager=self.manager,
        )
        self.password_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((170, 100), (300, 30)),
            manager=self.manager
        )
        self.nickname_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((170, 50), (300, 30)),
            manager=self.manager
        )
        self.password_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 100), (150, 30)),
            text=self.text_password,
            manager=self.manager
        )
        self.nickname_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 50), (150, 30)),
            text=self.text_nickname,
            manager=self.manager
        )

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def transition(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        print('hahaha')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Entrance().run()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Registration:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.language_selection()
        self.InitUI()
        self.loading_data()
        self.running = True

    def language_selection(self):
        if language == 'english':
            self.login = 'Register'
            self.text_password = 'Password:'
            self.text_nickname = 'Nickname:'
        else:
            self.login = 'Зарегистрироваться'
            self.text_password = 'Пароль:'
            self.text_nickname = 'Прозвище:'

    def InitUI(self):
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 500), (300, 60)),
            text=self.login,
            manager=self.manager,
        )
        self.password_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((160, 250), (250, 30)),
            manager=self.manager
        )
        self.nickname_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((160, 300), (250, 30)),
            manager=self.manager
        )
        self.password_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 300), (150, 30)),
            text=self.text_password,
            manager=self.manager
        )
        self.nickname_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 250), (150, 30)),
            text=self.text_nickname,
            manager=self.manager
        )

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.version = load_image('sprites/decoration/main/version.png', color_key=-1)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def transition(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.login_button:
                        print('hahaha')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Entrance().run()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Main:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.language_selection()
        self.InitUI()
        self.loading_data()
        self.running = True

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Main menu')
            self.play_button_text = 'Play'
            self.shop_button_text = 'Shop'
            self.settings_button_text = 'Settings'
            self.about_button_text = 'About'
            self.exit_button_text = 'Exit'
            self.question = 'Do you really want to go out?'
        else:
            pygame.display.set_caption('Главное меню')
            self.play_button_text = 'Играть'
            self.shop_button_text = 'Магазин'
            self.settings_button_text = 'Настройки'
            self.about_button_text = 'Об игре'
            self.exit_button_text = 'Выход'
            self.question = 'Вы правда хотите выйти?'

    def InitUI(self):
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 150), (300, 60)),
            text=self.play_button_text,
            manager=self.manager,
        )
        self.shop_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 220), (300, 60)),
            text=self.shop_button_text,
            manager=self.manager
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 290), (300, 60)),
            text=self.settings_button_text,
            manager=self.manager
        )
        self.about_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 360), (300, 60)),
            text=self.about_button_text,
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 430), (300, 60)),
            text=self.exit_button_text,
            manager=self.manager
        )

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.version = load_image('sprites/decoration/main/version.png', color_key=-1)
        self.sound_on_button = load_image('sprites/decoration/main/sound_on.png', color_key=-1)
        self.sound_off_button = load_image('sprites/decoration/main/sound_off.png', color_key=-1)
        self.rating_button = load_image('sprites/decoration/main/rating.png', color_key=-1)
        self.hide_button = load_image('sprites/decoration/main/hide.png', color_key=-1)

    def add_sprites(self):
        Rating_button(menu_button_sprites)
        Sound_button(menu_button_sprites)
        Roll_up_button(menu_button_sprites)
        Player(load_image("sprites/birds/blue_bird_glasses.png"), 4, 1, 50, 50, menu_image=True)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        player_sprite.draw(self.screen)
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        menu_button_sprites.draw(self.screen)
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def transition(self):
        full_cleaning_sprites()
        self.running = False

    def show_confirmation_dialog(self):
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((100, 150), (300, 200)),
            manager=self.manager,
            window_title='Exit',
            action_long_desc=self.question,
            action_short_name='Yes',
            blocking=True
        )

    def run(self):
        self.add_sprites()
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        self.transition()
                        Game().run()
                    if event.ui_element == self.shop_button:
                        self.transition()
                        Shop().run()
                    if event.ui_element == self.settings_button:
                        print('Settings pressed')
                    if event.ui_element == self.about_button:
                        print('About pressed')
                    if event.ui_element == self.exit_button:
                        self.show_confirmation_dialog()
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    self.transition()
                    sys.exit()
                menu_button_sprites.update(event)
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Game:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.language_selection()
        self.processes()
        self.loading_data()

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Game')
        else:
            pygame.display.set_caption('Игра')

    def processes(self):
        self.running = True
        self.score = -(COUNT_PIPES // 2)
        self.stop = False

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')
        self.wallUp = load_image("sprites/decoration/game/bottom_pipe.png")
        self.wallDown = load_image("sprites/decoration/game/top_pipe.png")

    def add_sprites(self):
        Player(load_image("sprites/birds/blue_bird_glasses.png"), 4, 1, 50, 50)

    def rendering(self):
        # rendering sprites
        self.screen.blit(self.background, (0, 0))
        background_sprites.draw(self.screen)
        pipe_sprites.draw(self.screen)
        ticket_sprites.draw(self.screen)
        player_sprite.draw(self.screen)
        self.font = pygame.font.SysFont("Arial", 50)
        self.screen.blit(self.font.render(str(self.score), -1, '#c76906'), (500, 10))
        # updating sprites
        if self.stop == False:
            if len(background_sprites) < COUNT_TILES_BACKGROUND:
                Background_sprite(temporary_sprites)
            background_sprites.update()
            if len(pipe_sprites) < COUNT_PIPES:
                self.score += 1
                Top_pipe(temporary_sprites)
                Bottom_pipe(temporary_sprites)
            pipe_sprites.update()
            ticket_sprites.update()
            player_sprite.update()

    def run(self):
        self.add_sprites()
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    full_cleaning_sprites()
                    self.running = False
                    Main().run()
                if key[pygame.K_LSHIFT]:
                    self.stop = not self.stop
            self.rendering()
            if len(player_sprite) == 0:
                full_cleaning_sprites()
                global score
                score = self.score
                self.running = False
                Final().run()
            pygame.display.update()


class Final:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.language_selection()
        self.processes()
        self.loading_data()

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Main menu')
            self.headline = 'Game over'
            self.points_text = 'points'
            self.prompt_text1 = 'Click on K to start a new game'
            self.prompt_text2 = 'Press Esc to exit to the menu'
        else:
            self.headline = 'Конец игры'
            self.points_text = 'очков'
            self.prompt_text1 = 'Нажмите K, чтобы начать новую игру'
            self.prompt_text2 = 'Нажмите Esc, чтобы выйти в меню'

    def processes(self):
        self.running = True

    def loading_data(self):
        self.coin = load_image('sprites/decoration/game/coin.png', color_key=-1)

    def rendering(self):
        intro_text = [(self.headline, 40, 120), (f'+{score // 5}', 15, 60),
                      (f'{score} {self.points_text}', 80, 60),
                      (self.prompt_text1, 15, 45),
                      (self.prompt_text2, 30, 45)]
        self.screen.fill('#e2b606')
        self.screen.blit((self.coin), (140, 235))
        text_coord = 50
        for text, coord, fnt in intro_text:
            font = pygame.font.SysFont("Arial", fnt)
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 50
            intro_rect.top = text_coord
            text_coord += coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while self.running:
            clock.tick(FPS)
            self.rendering()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    full_cleaning_sprites()
                    if event.key == pygame.K_k:
                        self.running = False
                        Game().run()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        main_music_play()
                        Main().run()
            pygame.display.update()


class Shop:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.processes()
        self.loading_data()
        self.loading_database()
        self.language_selection()
        self.InitUI()

    def language_selection(self):
        if language == 'english':
            self.select_button_text = 'Select'
        else:
            self.select_button_text = 'Выбрать'

    def processes(self):
        self.running = True
        self.select_background = 1
        self.con = sqlite3.connect('data/Database.db')
        self.cur = self.con.cursor()

    def InitUI(self):
        self.player_left_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 300), (90, 50)),
            text='<',
            manager=self.manager
        )
        self.player_right_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((460, 300), (90, 50)),
            text='>',
            manager=self.manager
        )
        self.player_select_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 300), (300, 50)),
            text=self.select_button_text,
            manager=self.manager
        )
        self.background_left_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 500), (90, 50)),
            text='<',
            manager=self.manager
        )
        self.background_right_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((460, 500), (90, 50)),
            text='>',
            manager=self.manager
        )
        self.background_select_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 500), (300, 50)),
            text=self.select_button_text,
            manager=self.manager
        )

    def loading_data(self):
        self.coin = load_image('sprites/decoration/game/coin.png', color_key=-1)
        self.background = load_image(f'sprites/decoration/backgrounds/{selected_background}/background.png')

    def loading_database(self):
        backgrounds = self.cur.execute("""SELECT * FROM Backgrounds""").fetchall()
        print(backgrounds)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        self.screen.blit((self.coin), (10, 15))
        font = pygame.font.SysFont("Arial", 40)
        self.screen.blit(font.render('100', -1, "#f0c106"), (70, 20))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.background_left_button:
                        print(1)
                    if event.ui_element == self.background_right_button:
                        print(2)
                    if event.ui_element == self.background_select_button:
                        print(3)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Main().run()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


if __name__ == "__main__":
    language = "english"
    pygame.font.init()
    Cursor(main_sprites)
    pygame.display.set_icon(pygame.image.load("data/sprites/decoration/icon.png"))
    main_music_play()
    Entrance().run()
    pygame.quit()