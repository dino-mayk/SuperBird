import sys, pygame_gui
from Sprites import *


# parameters
language = "english"
selected_bird = 'classic'
selected_background = ''


class Main:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600))
        self.InitUI()
        self.loading_data()
        self.processes()

    def processes(self):
        self.sound = True
        self.running = True

    def InitUI(self):
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 150), (300, 60)),
            text='Play',
            manager=self.manager,
        )
        self.shop_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 220), (300, 60)),
            text='Shop',
            manager=self.manager
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 290), (300, 60)),
            text='Settings',
            manager=self.manager
        )
        self.about_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 360), (300, 60)),
            text='About',
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 430), (300, 60)),
            text='Exit',
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
        if len(menu_sprites) < COUNT_TILES_MAIN:
            Tile_menu_background(temporary_sprites)
        menu_sprites.update()
        menu_sprites.draw(self.screen)
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        self.screen.blit(self.bird, (40, 80))
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        self.screen.blit(self.hide_button, (565, -10))
        self.screen.blit(self.rating_button, (0, 540))
        if self.sound is True:
            self.screen.blit(self.sound_on_button, (35, 550))
        else:
            self.screen.blit(self.sound_off_button, (35, 550))
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def run(self):
        if language == 'english':
            pygame.display.set_caption('Main menu')
        else:
            pygame.display.set_caption('Главное меню')
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        print('Game pressed')
                    if event.ui_element == self.shop_button:
                        print('Shop pressed')
                    if event.ui_element == self.settings_button:
                        print('Settings pressed')
                    if event.ui_element == self.about_button:
                        pass
                    if event.ui_element == self.exit_button:
                        pygame.quit()
                        sys.exit()
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


if __name__ == "__main__":
    Cursor(main_sprites)
    pygame.display.set_icon(pygame.image.load("data/sprites/decoration/icon.png"))
    music_play()
    Main().run()
    pygame.quit()