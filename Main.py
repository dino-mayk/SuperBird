import sys, pygame_gui
import Sprites
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
        self.size = self.width, self.height = (400, 400)
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.processes()
        self.loading_data()
        self.InitUI()

    def processes(self):
        self.running = True

    def loading_data(self):
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)

    def InitUI(self):
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 100), (300, 60)),
            text='Login',
            manager=self.manager,
        )
        self.registration_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 170), (300, 60)),
            text='Registration',
            manager=self.manager
        )
        self.account_creation_help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 240), (300, 60)),
            text='Account creation help',
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((50, 310), (300, 60)),
            text='Exit',
            manager=self.manager
        )

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.main_text, (20, -20))
        version_font = pygame.font.SysFont('Segoe Print', 10)
        version_text = version_font.render("Version 1.0", True, (255, 255, 255))
        self.screen.blit(version_text, (335, 380))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def show_confirmation_dialog(self):
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((100, 150), (300, 200)),
            manager=self.manager,
            window_title='Exit',
            action_long_desc='Are you sure you want to log out?',
            action_short_name='Yes',
            blocking=True
        )

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
                    if event.ui_element == self.account_creation_help_button:
                        Reference().run()
                    if event.ui_element == self.exit_button:
                        self.show_confirmation_dialog()
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    self.running = False
                    sys.exit()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Login:
    def __init__(self):
        self.size = self.width, self.height = LOGIN_AND_REGISTRATION_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager(LOGIN_AND_REGISTRATION_SCREEN, 'data/sprites/decoration/theme.json')
        self.processes()
        self.loading_data()
        self.InitUI()

    def processes(self):
        self.running = True
        self.error_message = False

    def loading_data(self):
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')

    def InitUI(self):
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 100), (350, 60)),
            text='Login',
            manager=self.manager,
        )
        self.password_label = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((100, 50), (250, 30)),
            manager=self.manager
        )
        self.login_label = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((100, 10), (250, 30)),
            manager=self.manager
        )

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        login_font = pygame.font.SysFont('Segoe Print', 13)
        login_text = login_font.render("login:", True, (255, 255, 255))
        self.screen.blit(login_text, (20, 10))
        password_font = pygame.font.SysFont('Segoe Print', 13)
        password_text = password_font.render("password:", True, (255, 255, 255))
        self.screen.blit(password_text, (20, 50))
        if self.error_message == True:
            error_message_font = pygame.font.SysFont('Segoe Print', 15)
            error_message_text = error_message_font.render("You entered incorrect data", True, (255, 0, 0))
            self.screen.blit(error_message_text, (90, 160))
        try:
            self.manager.update(self.time_delta)
        except Exception:
            pass
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def database_search(self):
        self.con = sqlite3.connect('data/Database.db')
        self.cur = self.con.cursor()
        projected_data = self.cur.execute(f"""SELECT * FROM Users""").fetchall()
        input_login = self.login_label.text
        input_password = self.password_label.text
        for user_id, user_login, user_password, gold, max_result, selected_skin, \
            selected_background, selected_language, sound_status, user_skins in projected_data:
            if input_login == input_login and user_password == input_password:
                global user
                global record
                global language
                global skin_id
                global skin
                global background
                global skins
                user = user_id
                record = max_result
                language = selected_language
                skin_id = selected_skin - 1
                skin = self.cur.execute(f"""SELECT name FROM Skins WHERE id = {selected_skin}""").fetchone()
                skin = skin[0]
                background = selected_background
                Sprites.sound = sound_status
                skins = str(user_skins)
                self.con.close()
                Main().run()
        self.error_message = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    try:
                        self.database_search()
                    except Exception:
                        self.error_message = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Entrance().run()
                try:
                    self.manager.process_events(event)
                except Exception:
                    pass
            self.rendering()
            pygame.display.update()


class Registration:
    def __init__(self):
        self.size = self.width, self.height = LOGIN_AND_REGISTRATION_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager(LOGIN_AND_REGISTRATION_SCREEN, 'data/sprites/decoration/theme.json')
        self.processes()
        self.loading_data()
        self.InitUI()

    def processes(self):
        self.running = True
        self.error_message = False

    def loading_data(self):
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')

    def InitUI(self):
        self.login_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((100, 10), (250, 30)),
            manager=self.manager
        )
        self.password_line = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((100, 50), (250, 30)),
            manager=self.manager
        )
        self.register_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((15, 100), (350, 60)),
            text='Register',
            manager=self.manager,
        )

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.SysFont('Segoe Print', 13)
        login_text = font.render("login:", True, (255, 255, 255))
        password_text = font.render("password:", True, (255, 255, 255))
        self.screen.blit(login_text, (20, 10))
        self.screen.blit(password_text, (20, 50))
        if self.error_message == True:
            error_message_font = pygame.font.SysFont('Segoe Print', 15)
            error_message_text = error_message_font.render("The data is incorrect or such "
                                                           "a login already exists", True, (255, 0, 0))
            self.screen.blit(error_message_text, (10, 160))
        try:
            self.manager.update(self.time_delta)
        except Exception:
            pass
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def add_database(self):
        try:
            self.con = sqlite3.connect('data/Database.db')
            self.cur = self.con.cursor()
            # addition variables
            input_login = self.login_line.text
            input_password = self.password_line.text
            # check
            if login_check(input_login) is False or password_check(input_password) is False:
                self.error_message = True
            else:
                # addition to the database
                self.cur.execute("""INSERT INTO Users(login, password, gold, max_result, selected_skin, 
                        selected_background, language, sound_status, user_skins) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (input_login,
                                                            input_password, 0, 0, 1, 1, 'english', '1', '1'))
                self.con.commit()
                self.con.close()
                self.running = False
                Login().run()
        except sqlite3.IntegrityError:
            self.error_message = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.add_database()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Entrance().run()
                try:
                    self.manager.process_events(event)
                except Exception:
                    pass
            self.rendering()
            pygame.display.update()


class Reference:
    def __init__(self):
        self.size = self.width, self.height = LOGIN_AND_REGISTRATION_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.processes()

    def processes(self):
        self.running = True

    def rendering(self):
        self.screen.fill('#e2b606')
        intro_text = [('Dear user, your login must be between 5 and 20', 10, 20),
                      ('characters long and original ;)', 20, 20),
                      ('And if there are problems with the password,', 10, 20),
                      ('then come up with it in size from 8 to 20 characters.', 20, 20)]
        text_coord = 30
        for text, coord, fnt in intro_text:
            font = pygame.font.SysFont("Arial", fnt)
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 10
            intro_rect.top = text_coord
            text_coord += coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Entrance().run()
            self.rendering()
            pygame.display.update()


class Main:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.processes()
        self.language_selection()
        self.InitUI()
        self.loading_data()

    def processes(self):
        self.running = True

    def loading_data(self):
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')
        self.player = load_image(f'sprites/birds/{skin}.png')
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.sound_on_button = load_image('sprites/decoration/main/sound_on.png', color_key=-1)
        self.sound_off_button = load_image('sprites/decoration/main/sound_off.png', color_key=-1)
        self.rating_button = load_image('sprites/decoration/main/rating.png', color_key=-1)
        self.hide_button = load_image('sprites/decoration/main/hide.png', color_key=-1)

    def add_sprites(self):
        Rating_button(menu_button_sprites)
        Sound_button(menu_button_sprites)
        Roll_up_button(menu_button_sprites)

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

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        self.screen.blit(self.player, (90, 90), (0, 0, 34, 50))
        version_font = pygame.font.SysFont('Segoe Print', 10)
        version_text = version_font.render("Version 1.0", True, (255, 255, 255))
        self.screen.blit(version_text, (530, 580))
        self.screen.blit(self.main_text, (120, 20))
        menu_button_sprites.draw(self.screen)
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def show_confirmation_dialog(self):
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((100, 150), (300, 200)),
            manager=self.manager,
            window_title='Exit',
            action_long_desc=self.question,
            action_short_name='Yes',
            blocking=True
        )

    def transition(self):
        full_cleaning_sprites()
        self.running = False

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
                        About().run()
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
        self.processes()
        self.loading_data()
        self.language_selection()

    def processes(self):
        self.running = True
        self.stop = False

    def loading_data(self):
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')
        self.wallUp = load_image("sprites/decoration/game/bottom_pipe.png")
        self.wallDown = load_image("sprites/decoration/game/top_pipe.png")

    def add_sprites(self):
        Player(load_image(f"sprites/birds/{skin}.png"), 4, 1, 50, 50)

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Game')
        else:
            pygame.display.set_caption('Игра')

    def rendering(self):
        # rendering sprites
        self.screen.blit(self.background, (0, 0))
        background_sprites.draw(self.screen)
        pipe_sprites.draw(self.screen)
        ticket_sprites.draw(self.screen)
        player_sprite.draw(self.screen)
        self.font = pygame.font.SysFont("Arial", 50)
        self.screen.blit(self.font.render(str(Sprites.score), -1, '#c76906'), (HEIGHT_SCREEN * 0.5, 10))
        # updating sprites
        if self.stop == False:
            if len(background_sprites) < COUNT_TILES_BACKGROUND:
                Background_sprite(temporary_sprites)
            background_sprites.update()
            if len(pipe_sprites) < COUNT_PIPES:
                Top_pipe(temporary_sprites)
                Bottom_pipe(temporary_sprites)
            pipe_sprites.update()
            ticket_sprites.update()
            player_sprite.update()

    def transition(self):
        full_cleaning_sprites()
        self.running = False

    def run(self):
        self.add_sprites()
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    update_gold(user, Sprites.score)
                    Sprites.score = 0
                    self.transition()
                    Main().run()
                if key[pygame.K_LSHIFT]:
                    self.stop = not self.stop
            self.rendering()
            if len(player_sprite) == 0:
                self.transition()
                Final().run()
            pygame.display.update()


class Final:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.processes()
        self.loading_data()
        self.language_selection()

    def processes(self):
        self.running = True
        tickets_coins = sum([random.randrange(1, MAX_TICKET_PRICE + 1) for ticket in range(Sprites.count_tickets)])
        coins = Sprites.score // COIN_POINT_RATIO
        self.count_coins = tickets_coins + coins
        # fixing a record and updating the number of coins
        if record < Sprites.score:
            self.con = sqlite3.connect('data/Database.db')
            self.cur = self.con.cursor()
            self.cur.execute(f"""UPDATE Users SET max_result = {Sprites.score} WHERE id = {user}""")
            self.con.commit()
            self.con.close()

    def loading_data(self):
        self.coin = load_image('sprites/decoration/game/coin.png', color_key=-1)
        self.ticket = load_image('sprites/decoration/game/ticket.png')

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

    def rendering(self):
        self.screen.fill('#e2b606')
        intro_text = [(self.headline, 20, 120), (f'+ {self.count_coins}', 10, 60),
                      (f'+ {Sprites.score} {self.points_text}', 10, 60),
                      (f'+ {Sprites.count_tickets}', 40, 60),
                      (self.prompt_text1, 15, 45),
                      (self.prompt_text2, 30, 45)]
        self.screen.blit((self.coin), (150, 195))
        self.screen.blit((self.ticket), (160, 350))
        text_coord = 30
        for text, coord, fnt in intro_text:
            font = pygame.font.SysFont("Arial", fnt)
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 50
            intro_rect.top = text_coord
            text_coord += coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def transition(self):
        full_cleaning_sprites()
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    full_cleaning_sprites()
                    if event.key == pygame.K_k:
                        update_gold(user, Sprites.score // COIN_POINT_RATIO)
                        Sprites.score = 0
                        Sprites.count_tickets = 0
                        self.transition()
                        Game().run()
                    if event.key == pygame.K_ESCAPE:
                        update_gold(user, Sprites.score // COIN_POINT_RATIO)
                        Sprites.score = 0
                        Sprites.count_tickets = 0
                        self.transition()
                        Main().run()
            self.rendering()
            pygame.display.update()


class Shop:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'data/sprites/decoration/theme.json')
        self.processes()
        self.loading_data()
        self.language_selection()
        self.InitUI()

    def language_selection(self):
        if language == 'english':
            self.select_button_text = 'Selected'
        else:
            self.select_button_text = 'Выбрано'

    def processes(self):
        self.running = True
        self.con = sqlite3.connect('data/Database.db')
        self.cur = self.con.cursor()
        self.shop_skins = self.cur.execute("""SELECT * FROM Skins""").fetchall()
        self.backgrounds = self.cur.execute("""SELECT * FROM Backgrounds""").fetchall()
        self.gold = self.cur.execute(f"""SELECT gold FROM Users WHERE id = {user}""").fetchone()[0]
        self.considered_skin = skin_id
        self.considered_background = 0

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
        self.background = load_image(f'sprites/backgrounds/{selected_background}/background.png')
        self.coin = load_image('sprites/decoration/game/coin.png', color_key=-1)
        self.player = load_image(f'sprites/birds/{self.shop_skins[self.considered_skin][-2]}.png')

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        self.screen.blit(self.player, (280, 230), (0, 0, 34, 50))
        self.screen.blit((self.coin), (10, 15))
        font = pygame.font.SysFont("Arial", 40)
        self.screen.blit(font.render(str(self.gold), -1, "#f0c106"), (70, 20))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        player_sprite.draw(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def select_skin(self):
        self.cur.execute(f"""UPDATE Users SET selected_skin = {self.considered_skin + 1} WHERE id = {user}""")

    def buy_skin(self):
        global skins
        global skin_id
        user_skins = self.cur.execute(f"""SELECT user_skins FROM Users WHERE id = {user}""").fetchone()[0]
        self.cur.execute(f"""UPDATE Users SET selected_skin = {self.considered_skin + 1},
                                             gold = {self.gold - self.shop_skins[self.considered_skin][-1]},
                                             user_skins = {str(user_skins) + str(self.considered_skin + 1)}
                                             WHERE id = {user}""")
        self.gold = self.gold - self.shop_skins[self.considered_skin][-1]
        skins = f'{skins}{self.considered_skin + 1}'
        skin_id = self.considered_skin + 1

    def change_select_button_text(self):
        if language == 'english':
            if self.considered_skin + 1 == skin_id:
                self.player_select_button.set_text('Selected')
            if str(self.considered_skin + 1) in skins:
                self.player_select_button.set_text('Select')
            if str(self.considered_skin + 1) not in skins:
                self.player_select_button.set_text('Buy')
        else:
            if self.considered_skin + 1 == skin_id:
                self.player_select_button.set_text('Выбрано')
            if str(self.considered_skin + 1) in skins:
                self.player_select_button.set_text('Выбрать')
            if str(self.considered_skin + 1) not in skins:
                self.player_select_button.set_text('Купить')

    def transition(self):
        full_cleaning_sprites()
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.player_left_button:
                        self.considered_skin -= 1
                        if self.considered_skin < 0:
                            self.considered_skin = len(self.shop_skins) - abs(self.considered_skin)
                    if event.ui_element == self.player_right_button:
                        self.considered_skin += 1
                        if self.considered_skin > len(self.shop_skins) - 1:
                            self.considered_skin = self.considered_skin - len(self.shop_skins)
                    if event.ui_element == self.player_select_button:
                        global skin
                        if self.shop_skins[self.considered_skin][-1] <= self.gold \
                                and str(self.considered_skin + 1) not in skins:
                            self.buy_skin()
                        else:
                            self.select_skin()
                        self.con.commit()
                        skin = self.shop_skins[self.considered_skin][1]
                        self.change_select_button_text()
                    if event.ui_element == self.background_left_button:
                        pass
                    if event.ui_element == self.background_right_button:
                        pass
                    if event.ui_element == self.background_select_button:
                        pass
                    self.change_select_button_text()
                    # change the image of the selected skin
                    self.player = load_image(f'sprites/birds/{self.shop_skins[self.considered_skin][-2]}.png')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.transition()
                        Main().run()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class About:
    def __init__(self):
        self.size = self.width, self.height = WIDTH_SCREEN, HEIGHT_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.language_selection()
        self.processes()

    def language_selection(self):
        if language == 'english':
            self.line1 = 'The game consists in the fact that you need to control the bird with'
            self.line2 = 'the space bar. It should fly between the pipes.'
            self.line3 = 'Shift - stop or continue the game'
            self.line4 = 'Esc - log off play or shop or settings or about'
            self.line5 = 'collect everything to try your luck'
            self.line6 = 'earn points and get for them'
            self.line7 = 'Course 5 to 1'
        else:
            self.line1 = 'Игра заключается в том, что надо с помощью пробела управлять'
            self.line2 = 'птичкой. Она должна пролетать между труб.'
            self.line3 = 'Shift - остановить или продолжить игру'
            self.line4 = 'Esc - выйти из игры или магазина или настроек или об игре'
            self.line5 = 'Собирай все и испытай свою удачу'
            self.line6 = 'Зарабатывай баллы и меняй их на монетки'
            self.line7 = 'Курс 5 к 1'

    def processes(self):
        self.running = True

    def rendering(self):
        self.screen.fill('#e2b606')
        intro_text = [(f'{self.line1}', 10, 30),
                      (f'{self.line2}', 20, 30),
                      (f'{self.line3}', 10, 30),
                      (f'{self.line4}', 20, 30),
                      (f'{self.line5}', 20, 30),
                      (f'{self.line6}', 20, 30),
                      (f'{self.line7}', 20, 30)]
        text_coord = 30
        for text, coord, fnt in intro_text:
            font = pygame.font.SysFont("Arial", fnt)
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 10
            intro_rect.top = text_coord
            text_coord += coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def transition(self):
        self.running = False

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while self.running:
            clock.tick(FPS)
            self.rendering()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.transition()
                        Main().run()
            pygame.display.update()



# class Rating:
# con = sqlite3.connect('название БД')
#cur = con.cursor()
#data = cur.execute("""SELECT login, max_result FROM USERS)


if __name__ == "__main__":
    pygame.font.init()
    Cursor(main_sprites)
    pygame.display.set_icon(pygame.image.load("data/sprites/decoration/icon.png"))
    Entrance().run()
    pygame.quit()