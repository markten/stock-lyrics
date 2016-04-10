import pygame
import color

TITLE = "Stock Lyrics"
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600
WORD_SPACING = 400
SCROLL_SPEED = 5

class TickerView(object):

    def __init__(self, original_lyrics, symbol_lyrics):
        pygame.init()
        self.screen_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.screen.fill(color.BLACK)
        self.font = pygame.font.Font("nokiafc22.ttf", 60)
        self.clock = pygame.time.Clock()

        self.text_position = WINDOW_SIZE_X

        self.original_lyric_graphics, self.symbol_lyric_graphics = self.generate_lyric_graphics(original_lyrics, symbol_lyrics, WORD_SPACING)

        self.running = True

        # make LED mask
        self.led_mask1 = pygame.Surface((WINDOW_SIZE_X, 100), pygame.SRCALPHA)

        for x in range(5, 600, 5):
            for y in range(5, 100, 5):
                pygame.draw.circle(self.led_mask1, color.WHITE, [x,y], 2)

        self.led_mask2 = pygame.Surface((WINDOW_SIZE_X, 100), pygame.SRCALPHA)

        for x in range(5, 600, 5):
            for y in range(5, 350, 5):
                pygame.draw.circle(self.led_mask2, color.WHITE, [x,y], 2)

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
        pygame.draw.rect(self.screen, color.BLACK, [0, 150, WINDOW_SIZE_X, 100])
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, 150], [ WINDOW_SIZE_X, 150], 3)
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, 150+100], [ WINDOW_SIZE_X, 150+100], 3)

        # Draw lower ticker
        pygame.draw.rect(self.screen, color.BLACK, [0, 350, WINDOW_SIZE_X, 100])
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, 350], [ WINDOW_SIZE_X, 350], 3)
        pygame.draw.line(self.screen, color.DARK_GRAY, [ 0, 350+100], [ WINDOW_SIZE_X, 350+100], 3)

        # Draw scrolling text
        for index, lyric in enumerate(self.original_lyric_graphics):
            if index < 4:
                masked = lyric.font_object.copy()
                masked.blit(self.led_mask1, [0,0], None, pygame.BLEND_RGBA_MULT)
                self.screen.blit(masked, [lyric.x_position, 150+20])
            lyric.x_position -= SCROLL_SPEED
            if lyric.x_position < -WORD_SPACING:
                self.original_lyric_graphics.remove(lyric)

        for index, lyric in enumerate(self.symbol_lyric_graphics):
            if index < 4:
                masked = lyric.font_object.copy()
                masked.blit(self.led_mask2, [0,0], None, pygame.BLEND_RGBA_MULT)
                self.screen.blit(masked, [lyric.x_position+150, 350+20])
            lyric.x_position -= SCROLL_SPEED
            if lyric.x_position < -WORD_SPACING:
                self.symbol_lyric_graphics.remove(lyric)

        # Print artist name and title


        pygame.display.flip()

    def generate_lyric_graphics(self, original_lyrics, symbol_lyrics, word_spacing):
        original_lyric_graphics = []
        symbol_lyric_graphics = []

        total_length = 0

        for word in original_lyrics.split():
            new_font_object = self.font.render(word, True, color.ORANGE)
            new_lyric_graphic = LyricGraphic(total_length, new_font_object)
            original_lyric_graphics.append(new_lyric_graphic)
            new_font_object = None

            total_length += word_spacing
            print total_length

        total_length = 0

        for word in symbol_lyrics.split():
            new_font_object = self.font.render(word, True, color.GREEN)
            new_lyric_graphic = LyricGraphic(total_length, new_font_object)
            symbol_lyric_graphics.append(new_lyric_graphic)
            new_font_object = None

            total_length += word_spacing
            print total_length

        return original_lyric_graphics, symbol_lyric_graphics


class LyricGraphic(object):

    def __init__(self, x_position, font_object):
        self.x_position = x_position
        self.font_object = font_object

if __name__ == '__main__':
    ticker = TickerView()
    ticker.run()
