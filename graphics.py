import pygame
import color

TITLE = "Stock Symphony"
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 600

class TickerView:

    def __init__(self):
        pygame.init()
        self.screen_size = (WINDOW_SIZE_X, WINDOW_SIZE_Y)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.screen.fill(color.BLACK)
        self.font = pygame.font.Font("nokiafc22.ttf", 62)
        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):

        while self.running:
            self.handle_events()
            self.draw_assets()
            self.clock.tick(20)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def draw_assets(self):
        self.screen.fill(color.LIGHT_GRAY)

        # Draw upper ticker
        pygame.draw.rect(self.screen, color.DARK_GRAY, [0, 150, WINDOW_SIZE_X, 100])
        pygame.draw.line(self.screen, color.BLACK, [ 0, 150], [ WINDOW_SIZE_X, 150], 3)
        pygame.draw.line(self.screen, color.BLACK, [ 0, 150+100], [ WINDOW_SIZE_X, 150+100], 3)

        # Draw lower ticker
        pygame.draw.rect(self.screen, color.DARK_GRAY, [0, 350, WINDOW_SIZE_X, 100])
        pygame.draw.line(self.screen, color.BLACK, [ 0, 350], [ WINDOW_SIZE_X, 350], 3)
        pygame.draw.line(self.screen, color.BLACK, [ 0, 350+100], [ WINDOW_SIZE_X, 350+100], 3)

        # Draw scrolling text
        original_text = self.font.render("TEST 1", True, color.ORANGE)
        symbol_text = self.font.render("TEST 2", True, color.ORANGE)
        self.screen.blit(original_text, [50, 150+50])
        self.screen.blit(symbol_text, [100, 350+50])

        pygame.display.flip()

if __name__ == '__main__':
    ticker = TickerView()
    ticker.run()
