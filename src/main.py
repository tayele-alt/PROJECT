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
        on_ground = False
    
        # Movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * delta
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * delta

        #Wall
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.right > SCREEN_WIDTH - 10:
            self.rect.right = SCREEN_WIDTH - 10

        #Jumpingg
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_power
            self.is_jumping = True

        #Gravityy
        self.velocity_y += self.gravity * delta
        self.rect.y += self.velocity_y * delta

        #Platform collision
        for plat in game_platforms:
            if self.rect.colliderect(plat.rect):
                if self.velocity_y >= 0 and self.rect.bottom <= plat.rect.bottom:
                    self.rect.bottom = plat.rect.top
                    self.velocity_y = 0
                    on_ground = True
                elif self.velocity_y < 0 and self.rect.top >=plat.rect.top:
                    self.rect.top = plat.rect.bottom
                    self.velocity_y = 0
        #Horizontal collision
        for plat in game_platforms:
            if self.rect.colliderect(plat.rect):
                if self.rect.centerx < plat.rect.centerx:
                    self.rect.right = plat.rect.left
                else:
                    self.rect.left = plat.rect.right
        self.is_jumping = not on_ground

        if self.has_flag:
            self.image.fill(YELLOW)
        else:
            self.image.fill(BLUE)


#Platorms
class Platfrom(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
        pygame.draw.rect(self.image, CYAN, (0, 0, w, 3))
        self.rect = self.image.get_rect(topleft=(x,y))

#Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40,60))
        self.image.fill(RED)
        pygame.draw.rect(self.image, ORANGE, (5, 5, 30, 20))
        self.rect = self.image.get_rect(bottomleft=(x,y))
        self.base_speed = 120
        self.speed = 120
        self.gravity = PLAYER_GRAVITY
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_timer = 0

    def update(self, delta, player, game_platforms):
        #To chase player horizontally
        if player.rect.centerx < self.rect.centerx:
            self.rect.x -= self.speed * delta
        else:
            self.rect.x += self.speed * delta

        #Gravity
        self.velocity_y += self.gravity * delta
        if self.velocity_y > 600:
            self.velocity_y = 600
        self.rect.y += self.velocity_y * delta

        #Platform collision
        for plat in game_platforms:
            if self.rect.colliderect(plat.rect):
                if self.velocity_y >= 0 and self.rect.bottom <= plat.rect.bottom:
                    self.rect.bottom = plat.rect.top
                    self.velocity_y = 0

        #Wall
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.left < 90:
            self.rect.left = 90
        if self.rect.right > SCREEN_WIDTH - 10:
            self.rect.right = SCREEN_WIDTH - 10

#Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((12,6))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(centery=y, x=x)
        self.speed = 400 * direction

    def update(self, delta, game_platforms=None):
        self.rect.x += self.speed * delta
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        if self.rect.right < 90 and self.speed < 0:
            self.kill()

#Enemy Bullet
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 300 * direction

    def update(self, delta, game_platforms=None):
        self.rect.x += self.speed * delta
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

#Gun
class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((18,18))
        self.image.fill(RED)
        pygame.draw.rect(self.image, ORANGE, ( 0, 6, 18, 6))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction
        self.shoot_interval = 2.5
        import random
        self.timer = random.uniform(0, 2.5)

    def update(self, delta, game_platforms=None):
        self.timer += delta


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
            (0, 480, 800, 20),
            (0, 0, 10, 500),
            (790, 0, 10, 500),
            (80, 370, 120, 12),
            (240, 310, 100, 12),
            (370, 250, 80, 12),
            (480, 310, 100, 12),
            (620, 360, 110, 12),
            (150, 200, 90, 12),
            (300, 150, 80, 12),
            (450, 170, 90, 12),
            (600, 200, 100, 12),
            (680, 280, 80, 12),
            (50, 290, 80, 12),
            (700, 130, 80, 12),
        ]:
            p = Platfrom(x, y, w, h)
            self.platforms.add(p)
            self.all_sprites.add(p)

        #Sprites
        self.player = Player()
        self.all_sprites.add(self.player)
        self.flag = Flag(720, 130)
        self.all_sprites.add(self.flag)


        self.enemy = Enemy(600, 480)
        self.guns = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        for (x, y, direction) in [
            (10, 150, 1),
            (790, 280, -1),
            (10, 380, 1),
            (790, 420, -1),
        ]:
            g = Gun(x, y, direction)
            self.guns.add(g)
            self.all_sprites.add(g)

        self.all_sprites.add(self.enemy)
        self.score = 0
        if not hasattr(self, 'high_score'):
            self.high_score = 0
        self.lives = 3
        self.time_left = GAME_DURATION
        self.font = pygame.font.SysFont(None, 36)

    def _player_hit(self):
        self.lives -= 1
        self.player.reset()
        self.enemy.rect.bottomleft = (600, 480)
        self.enemy.velocity_y = 0
        if self.lives <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
            self.running = False


    def _game_over_screen(self):
        self.screen.fill(BLACK)
        title = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        high_text = self.font.render(f"High Score: {self.high_score}", True, YELLOW)
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, GRAY)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 160))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 230))
        self.screen.blit(high_text, (SCREEN_WIDTH // 2 - high_text.get_width() // 2, 260))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()


    def _handle_events(self):
        running = not pygame.event.peek(pygame.QUIT)
        if not running:
            self.running = False
        pygame.event.clear()

    def _update(self, delta):
        self.time_left -= delta
        if self.time_left <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
            self.running = False

        self.player.update(delta, self.platforms)
        self.enemy.update(delta, self.player, self.platforms)

        #Shooting Gun
        for gun in self.guns:
            gun.timer += delta
            if gun.timer >= gun.shoot_interval:
                gun.timer = 0
                bx = gun.rect.right if gun.direction == 1 else gun.rect.left
                b = Bullet(bx, gun.rect.centery, gun.direction)
                self.bullets.add(b)
                self.all_sprites.add(b)

        self.bullets.update(self.clock.get_time() / 1000.0)

        #When bullet hits player
        for bullet in self.bullets:
            if bullet.rect.colliderect(self.player.rect):
                bullet.kill()
                if self.player.has_flag:
                    self.player.has_flag = False
                    self.flag = Flag(720, 130)
                    self.all_sprites.add(self.flag)
                self._player_hit()

        #Pickup the Flag
        if not self.flag.collected and self.player.rect.colliderect(self.flag.rect):
            self.flag.collected = True
            self.player.has_flag = True
            self.flag.kill()

        #Return flag to base
        if self.player.has_flag and self.player.rect.left <=60:
            self.player.has_flag = False
            self.score +=1
            self.enemy.speed = self.enemy.base_speed + (self.score * 20)
            self.flag = Flag(720, 130)
            self.all_sprites.add(self.flag)

        #When enemy catches player
        if self.player.rect.colliderect(self.enemy.rect):
            if self.player.has_flag:
                self.player.has_flag = False
                self.flag = Flag(720, 130)
                self.all_sprites.add(self.flag)
            self._player_hit()

    def _draw(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, (0, 60, 0), (0, 350, 90, 130))
        pygame.draw.rect(self.screen, GREEN, (0, 350, 90, 130), 2)
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, DARK_GRAY, (i, 0), (i, SCREEN_HEIGHT), 1)
        for i in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, DARK_GRAY, (0, i), (SCREEN_WIDTH, i), 1)
        pygame.draw.line(self.screen, GRAY, (0, SCREEN_HEIGHT -50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)
        self.all_sprites.draw(self.screen)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text,(10, 10))

        timer_text = self.font.render(f"Time: {int(self.time_left)}", True, WHITE)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 120, 10))

        lives_text = self.font.render (f"Lives: {self.lives}", True, RED)
        self.screen.blit(lives_text, (SCREEN_WIDTH // 2 - lives_text.get_width() // 2, 10))

        if self.player.has_flag:
            flag_text = self.font.render("Flag captured! Return to your base!", True, YELLOW)
            self.screen.blit(flag_text, (SCREEN_WIDTH // 2 - flag_text.get_width() // 2, 40))

        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_events()
            self.clock.tick(MAX_FPS)
            delta = self.clock.get_time() / 1000.0
            self._update(delta)
            self._draw()
        self._game_over_screen()

if __name__ == "__main__":
    game = Game()
    game.run()