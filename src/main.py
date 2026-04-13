import pygame
import os

GAME_TITLE = "Capture The Flag"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
MAX_FPS = 60

#Colors
WHITE = (225, 225, 225)
BLACK = (15, 15, 15)
BLUE = (70, 130, 255)
GREEN = (50, 200, 80)
RED = (220, 60, 60)
YELLOW = (225, 215, 0)
GRAY = (90, 100, 115)
DARK_GRAY = (40, 45, 55)
ORANGE = (255, 140, 0)
CYAN = (0, 220, 220)

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
        self.is_jumping = False
        self.velocity_y = 0
        self.has_flag = False

    def update(self, delta, game_platforms=None):
        keys = pygame.key.get_pressed()
    
        # Movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed * delta
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed * delta

        #Jumpingg
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_power

        #Gravityy
        if self.is_jumping:
            self.velocity_y += self.gravity * delta
            self.rect.y += self.velocity_y * delta

        #Platform collision
        self.is_jumping = True
        for plat in game_platforms:
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

#Flag
class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.collected = False

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
        self.all_sprites = pygame.sprite.Group()
        for (x, y, w, h) in [
            (0, 450, 800, 20),
            (100, 370, 150, 15),
            (320, 310, 150, 15),
            (550, 370, 150, 15),
            (200, 230, 130, 15),
            (470, 210, 130, 15),
        ]:
            p = Platfrom(x, y, w, h)
            self.platforms.add(p)
            self.all_sprites.add(p)

        #Sprites
        self.player = Player()
        self.all_sprites.add(self.player)

        self.flag = Flag(720, 180)
        self.all_sprites.add(self.flag)

        self.score = 0
        self.time_left = GAME_DURATION
        self.font = pygame.font.SysFont(None, 36)


    def _handle_events(self):
        running = not pygame.event.peek(pygame.QUIT)
        if not running:
            self.running = False
        pygame.event.clear()

    def _update(self, delta):
        self.time_left -= delta
        if self.time_left <= 0:
            self.running = False
        self.player.update(delta, self.platforms)
        for sprite in self.all_sprites:
            if sprite != self.player:
                sprite.update(delta)
#Pickup the Flag
            if not self.flag.collected and self.player.rect.colliderect(self.flag.rect):
                self.flag.collected = True
                self.player.has_flag = True
                self.flag.kill()

#Return flag to base
            if self.player.has_flag and self.player.rect.left <=60:
                self.player.has_flag = False
                self.score +=1
                self.flag = Flag(720, 180)
                self.all_sprites.add(self.flag)

    def _draw(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, GRAY, (0, SCREEN_HEIGHT -50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)
        self.all_sprites.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text,(10, 10))

        timer_text = self.font.render(f"Time: {int(self.time_left)}", True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 120, 10))

        if self.player.has_flag:
            flag_text = self.font.render("Flag captured! Return to your base!", True, YELLOW)
            self.screen.blit(flag_text, (180,10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_events()
            self.clock.tick(MAX_FPS)
            delta = self.clock.get_time() / 1000.0
            self._update(delta)
            self._draw()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()