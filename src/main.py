import pygame
import os

GAME_TITLE = "Capture The Flag"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
MAX_FPS = 60

#Colors
WHITE = (225, 225, 225)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)
GREEN = (50, 180, 50)
RED = (200, 50, 50)
YELLOW = (225, 215, 0)
GRAY = (120, 120, 120)

#Game Constants
PLAYER_SPEED = 300
PLAYER_JUMP_POWER = -600
PLAYER_GRAVITY = 1200
GAME_DURATION = 60

#Folder Path
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

#Game
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, delta):
        pass

    def _draw(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(MAX_FPS)
            delta = self.clock.get_time() / 1000.0
            self._update(delta)
            self._draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()