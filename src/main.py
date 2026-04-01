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

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.reset()
        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = PLAYER_GRAVITY
        self.is_jumping = False
        self.has_flag = False

    def reset(self):
        self.rect.bottomleft = (20, SCREEN_HEIGHT - 50)
        self.its_jumping = False
        self.velocity_y = 0
        self.has_flag = False

    def update(self, delta):
        keys = pygame.key.get_pressed()
    
        # Movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed * delta
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed * delta

        #Jumpingg
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = self.jump_power

        #Gravityy
        if self.is_jumping:
            self.velocity_y += self.gravity * delta
            self.rect.y += self.velocity_y * delta

        #Platform collision
        self.is_jumping = True
        for plat in game.platforms:
            if self.rect.colliderect(plat.rect) and self.velocity_y >=0:
                self.rect.bottom = plat.rect.top
                self.velocity_y = 0
                self.is_jumping = False


#Platorms
class Platfrom(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x,y))
#Game
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        #Platforms
        self.platforms = pygame.sprite.Group()
        for (x, y, w, h) in [
            (0, 450, 800, 20)
        ]:
            p = Platfrom(x, y, w, h)
            self.platforms.add(p)
            self.all_sprites(p)

        #Sprites
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)

    def _handle_events(self):
        running = not pygame.event.peek(pygame.QUIT)
        if not running:
            self.running = False
        pygame.event.clear()

    def _update(self, delta):
        self.all_sprites.update(delta)

    def _draw(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, GRAY, (0, SCREEN_HEIGHT -50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self,self._handle_events()
            self.clock.tick(MAX_FPS)
            delta = self.clock.get_time() / 1000.0
            self._update(delta)
            self._draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()