import pygame
import color
from random import randrange

TITLE = "Stock Lyrics"
WORD_SPACING = 500
BAR_HEIGHT = 100
SCROLL_SPEED = 10
X = 0
Y = 1

class TickerView(object):

    def __init__(self, original_lyrics, symbol_lyrics, song_title, song_artist):
        pygame.init()
        display_info = pygame.display.Info()
        self.screen_size = (display_info.current_w, display_info.current_h)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.screen.fill(color.BLACK)

        self.clock = pygame.time.Clock()

        self.font = self.load_fonts()
        self.led_mask = self.generate_led_mask()
        self.original_lyric_graphics = self.generate_lyric_graphics(original_lyrics, WORD_SPACING, color.ORANGE)
        self.symbol_lyric_graphics = self.generate_lyric_graphics(symbol_lyrics, WORD_SPACING, color.GREEN)

        self.heading_text = self.font['medium'].render(song_artist.replace('-', ' ').title() + ' -- ' + song_title.replace('-', ' ').title(), True, color.WHITE)
        self.heading_offset = int(self.font['medium'].size(song_artist + ' -- ' + song_title)[X]/2)
        self.help_text = self.font['medium'].render('Press q to exit.', True, color.WHITE)

        self.running = True

    def run(self):

        while self.running:
            self.handle_events()
            self.draw_assets()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

        if not self.original_lyric_graphics and not self.symbol_lyric_graphics:
            self.running = False

    def draw_assets(self):
        self.screen.fill(color.DARK_BLUE)

        # Draw upper ticker
        pygame.draw.rect(self.screen, color.BLACK,[0, int(0.2*self.screen_size[Y]),
                          self.screen_size[X], BAR_HEIGHT])
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, int(0.2*self.screen_size[Y])],
                         [self.screen_size[X], int(0.2*self.screen_size[Y])], 3)
        pygame.draw.line(self.screen, color.DARK_GRAY,[ 0, int(0.2*self.screen_size[Y])+BAR_HEIGHT],
                         [self.screen_size[X], int(0.2*self.screen_size[Y])+BAR_HEIGHT], 3)

        # Draw lower ticker
        pygame.draw.rect(self.screen, color.BLACK,
                         [0, int(0.8*self.screen_size[Y])-BAR_HEIGHT,self.screen_size[X], BAR_HEIGHT])
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, int(0.8*self.screen_size[Y])-BAR_HEIGHT],
                         [self.screen_size[X], int(0.8*self.screen_size[Y])-BAR_HEIGHT], 3)
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, int(0.8*self.screen_size[Y])],
                         [self.screen_size[X], int(0.8*self.screen_size[Y])], 3)

        # Draw scrolling text
        self.draw_lyric(self.original_lyric_graphics, int(0.2*self.screen_size[Y])+20)
        self.draw_lyric(self.symbol_lyric_graphics, int(0.8*self.screen_size[Y])-80)

        # Print artist name and title
        self.screen.blit(self.heading_text, [int(self.screen_size[X]/2) - self.heading_offset, 10])

        # print exit help
        self.screen.blit(self.help_text, [10, self.screen_size[Y]-30])

        pygame.display.flip()

    def draw_lyric(self, lyric_graphics, y_offset):
        for index, lyric in enumerate(lyric_graphics):
            if index < 5:
                self.screen.blit(lyric.font_object, [lyric.x_position, y_offset])
            lyric.x_position -= SCROLL_SPEED
            if lyric.x_position < -WORD_SPACING:
                lyric_graphics.remove(lyric)

    def generate_lyric_graphics(self, lyrics, word_spacing, text_color):
        lyric_graphics = []

        total_length = 0

        for word in lyrics.split():
            new_font_object = self.font['large'].render(word, True, text_color)
            new_font_object.blit(self.led_mask, [0,0], None, pygame.BLEND_RGBA_MULT)
            new_lyric_graphic = LyricGraphic(total_length + randrange(0, 100), new_font_object)
            lyric_graphics.append(new_lyric_graphic)
            new_font_object = None

            total_length += word_spacing

        total_length = 0

        return lyric_graphics

    def generate_led_mask(self):
        led_mask = pygame.Surface((self.screen_size[X], 100), pygame.SRCALPHA)

        for x in range(5, 600, 5):
            for y in range(5, 100, 5):
                pygame.draw.circle(led_mask, color.WHITE, [x,y], 2)

        return led_mask

    def load_fonts(self):
        font = {
            'large': pygame.font.Font("nokiafc22.ttf", 60),
            'medium': pygame.font.Font("nokiafc22.ttf", 24),
            'small': pygame.font.Font("nokiafc22.ttf", 12)
        }

        return font

class LyricGraphic(object):

    def __init__(self, x_position, font_object):
        self.x_position = x_position
        self.font_object = font_object

if __name__ == '__main__':
    ticker = TickerView()
    ticker.run()
