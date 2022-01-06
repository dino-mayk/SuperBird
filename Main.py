import pygame_gui
from Sprites import *



# parameters
language = "english"
selected_bird = 'classic'
selected_background = ''


class Main:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'theme.json')
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
            self.play_button_text = 'Играть'
            self.shop_button_text = 'Магазин'
            self.settings_button_text = 'Настройки'
            self.about_button_text = 'Об игре'
            self.exit_button_text = 'Выход'
            pygame.display.set_caption('Главное меню')
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
            text=self.shop_button_text,
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
        self.background = load_image(f'sprites/decoration/main/backgrounds/clouds/background.png')
        self.bird = load_image(f'sprites/birds/{selected_bird}.png', color_key=-1)
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.version = load_image('sprites/decoration/main/version.png', color_key=-1)
        self.sound_on_button = load_image('sprites/decoration/main/sound_on.png', color_key=-1)
        self.sound_off_button = load_image('sprites/decoration/main/sound_off.png', color_key=-1)
        self.rating_button = load_image('sprites/decoration/main/rating.png', color_key=-1)
        self.hide_button = load_image('sprites/decoration/main/hide.png', color_key=-1)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(menu_background_sprites) < COUNT_TILES_MAIN:
            Menu_background_sprite(temporary_sprites)
        menu_background_sprites.update()
        menu_background_sprites.draw(self.screen)
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        menu_button_sprites.draw(self.screen)
        self.screen.blit(self.bird, (40, 80))
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        Rating_button(menu_button_sprites)
        Sound_button(menu_button_sprites)
        Roll_up_button(menu_button_sprites)
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        self.running = False
                        #Game().run()
                    if event.ui_element == self.shop_button:
                        print('Shop pressed')
                    if event.ui_element == self.settings_button:
                        print('Settings pressed')
                    if event.ui_element == self.about_button:
                        print('About pressed')
                    if event.ui_element == self.exit_button:
                        exit_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pygame.Rect((100, 158), (300, 200)),
                            manager=self.manager,
                            window_title='Exit',
                            action_long_desc=self.question,
                            action_short_name='Yes',
                            blocking=True
                        )

                        # это на доработке
                menu_button_sprites.update(event)
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


if __name__ == "__main__":
    Cursor(main_sprites)
    pygame.display.set_icon(pygame.image.load("data/sprites/decoration/icon.png"))
    music_play()
    Main().run()
    pygame.quit()