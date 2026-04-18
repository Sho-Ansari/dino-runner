import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 300
GROUND_Y = 250
FPS = 60
GRAVITY = 0.8
JUMP_FORCE = -15
INITIAL_SPEED = 6
MAX_SPEED = 20
SPEED_INCREMENT = 0.001

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83)
DARK_GRAY = (50, 50, 50)
GREEN = (80, 140, 60)
SKY_BLUE = (235, 245, 255)
NIGHT_SKY = (25, 25, 50)
CLOUD_WHITE = (220, 220, 220)


class Dino:
    def __init__(self):
        self.x = 80
        self.normal_height = 60
        self.duck_height = 30
        self.width = 40
        self.height = self.normal_height
        self.y = GROUND_Y - self.height
        self.vel_y = 0
        self.on_ground = True
        self.ducking = False

    def jump(self):
        if self.on_ground and not self.ducking:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

    def duck(self, ducking):
        if ducking and not self.ducking and self.on_ground:
            self.ducking = True
            self.height = self.duck_height
            self.y = GROUND_Y - self.duck_height
        elif not ducking and self.ducking:
            self.ducking = False
            self.height = self.normal_height
            self.y = GROUND_Y - self.normal_height

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y >= GROUND_Y - self.height:
            self.y = GROUND_Y - self.height
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        if not self.ducking:
            pygame.draw.rect(screen, color, (self.x + 15, self.y - 20, 30, 25))
            pygame.draw.rect(screen, WHITE, (self.x + 33, self.y - 15, 8, 8))
            pygame.draw.rect(screen, BLACK, (self.x + 36, self.y - 13, 4, 4))
            pygame.draw.rect(screen, color, (self.x - 8, self.y + 10, 12, 6))
        else:
            pygame.draw.rect(screen, color, (self.x + 25, self.y - 10, 30, 15))
            pygame.draw.rect(screen, WHITE, (self.x + 45, self.y - 6, 6, 6))
            pygame.draw.rect(screen, BLACK, (self.x + 47, self.y - 4, 3, 3))
        leg_tick = (pygame.time.get_ticks() // 120) % 2
        if self.on_ground:
            pygame.draw.rect(screen, color, (self.x + 3, self.y + self.height, 10, 8 + leg_tick * 4))
            pygame.draw.rect(screen, color, (self.x + 23, self.y + self.height, 10, 8 + (1 - leg_tick) * 4))

    def get_rect(self):
        return pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 5)


class Cactus:
    def __init__(self, x):
        self.kind = random.choice(['small', 'large', 'group'])
        if self.kind == 'small':
            self.width, self.height = 20, 40
        elif self.kind == 'large':
            self.width, self.height = 28, 60
        else:
            self.width, self.height = 55, 45
        self.x = x
        self.y = GROUND_Y - self.height

    def update(self, speed):
        self.x -= speed

    def draw(self, screen):
        if self.kind == 'group':
            pygame.draw.rect(screen, GREEN, (self.x, self.y + 5, 18, self.height - 5))
            pygame.draw.rect(screen, GREEN, (self.x + 22, self.y, 16, self.height))
            pygame.draw.rect(screen, GREEN, (self.x + 42, self.y + 10, 13, self.height - 10))
        else:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
            arm_y = self.y + self.height // 3
            pygame.draw.rect(screen, GREEN, (self.x - 8, arm_y, 8, 6))
            pygame.draw.rect(screen, GREEN, (self.x - 8, arm_y - 12, 6, 12))
            pygame.draw.rect(screen, GREEN, (self.x + self.width, arm_y + 8, 8, 6))
            pygame.draw.rect(screen, GREEN, (self.x + self.width + 2, arm_y - 4, 6, 12))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def off_screen(self):
        return self.x + self.width < 0


class Bird:
    def __init__(self, x):
        self.x = x
        self.y = random.choice([GROUND_Y - 90, GROUND_Y - 130, GROUND_Y - 50])
        self.width = 40
        self.height = 22
        self.wing_up = True
        self.wing_timer = 0

    def update(self, speed):
        self.x -= speed * 1.05
        self.wing_timer += 1
        if self.wing_timer > 12:
            self.wing_up = not self.wing_up
            self.wing_timer = 0

    def draw(self, screen):
        pygame.draw.ellipse(screen, DARK_GRAY, (self.x, self.y, self.width, self.height))
        if self.wing_up:
            pygame.draw.ellipse(screen, GRAY, (self.x + 5, self.y - 14, 28, 18))
        else:
            pygame.draw.ellipse(screen, GRAY, (self.x + 5, self.y + 6, 28, 18))
        pygame.draw.polygon(screen, (220, 160, 60), [
            (self.x + self.width, self.y + self.height // 2 - 3),
            (self.x + self.width + 10, self.y + self.height // 2),
            (self.x + self.width, self.y + self.height // 2 + 3),
        ])
        pygame.draw.circle(screen, WHITE, (self.x + self.width - 6, self.y + self.height // 2 - 2), 3)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 5, self.y + self.height // 2 - 2), 2)

    def get_rect(self):
        return pygame.Rect(self.x + 4, self.y + 2, self.width - 8, self.height - 4)

    def off_screen(self):
        return self.x + self.width < 0


class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(60, 110)
        self.height = 24

    def update(self, speed):
        self.x -= speed * 0.3

    def draw(self, screen):
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, CLOUD_WHITE, (self.x + 15, self.y - 12, self.width - 25, self.height + 4))

    def off_screen(self):
        return self.x + self.width < 0


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dino Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 22, bold=True)
        self.big_font = pygame.font.SysFont("consolas", 48, bold=True)
        self.small_font = pygame.font.SysFont("consolas", 16)
        self.high_score = 0
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = []
        self.clouds = [Cloud(random.randint(0, WIDTH), random.randint(30, 100)) for _ in range(3)]
        self.speed = INITIAL_SPEED
        self.score = 0
        self.game_over = False
        self.started = False
        self.spawn_timer = 0
        self.cloud_timer = 0
        self.night_mode = False
        self.night_timer = 0
        self.ground_x = 0

    def spawn_obstacle(self):
        x = WIDTH + 50
        if self.score > 400 and random.random() < 0.3:
            self.obstacles.append(Bird(x))
        else:
            self.obstacles.append(Cactus(x))

    def check_collision(self):
        dino_rect = self.dino.get_rect()
        for obs in self.obstacles:
            if dino_rect.colliderect(obs.get_rect()):
                return True
        return False

    def update(self):
        if self.game_over or not self.started:
            return
        self.score += 1
        self.speed = min(INITIAL_SPEED + self.score * SPEED_INCREMENT, MAX_SPEED)
        self.night_timer += 1
        if self.night_timer > 800:
            self.night_mode = not self.night_mode
            self.night_timer = 0
        self.dino.update()
        self.spawn_timer += 1
        min_gap = max(55, 95 - int(self.score / 150))
        if self.spawn_timer > min_gap + random.randint(0, 45):
            self.spawn_obstacle()
            self.spawn_timer = 0
        self.cloud_timer += 1
        if self.cloud_timer > 140:
            self.clouds.append(Cloud(WIDTH + 50, random.randint(30, 100)))
            self.cloud_timer = 0
        for obs in self.obstacles:
            obs.update(self.speed)
        for cloud in self.clouds:
            cloud.update(self.speed)
        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        self.clouds = [c for c in self.clouds if not c.off_screen()]
        self.ground_x = (self.ground_x - self.speed) % 40
        if self.check_collision():
            self.game_over = True
            self.high_score = max(self.high_score, self.score)

    def draw(self):
        bg = NIGHT_SKY if self.night_mode else SKY_BLUE
        fg = WHITE if self.night_mode else BLACK
        dino_color = WHITE if self.night_mode else GRAY
        self.screen.fill(bg)
        for cloud in self.clouds:
            cloud.draw(self.screen)
        pygame.draw.line(self.screen, fg, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
        for x in range(-40, WIDTH + 40, 40):
            pygame.draw.rect(self.screen, fg, (x + self.ground_x, GROUND_Y + 4, 14, 3))
            pygame.draw.rect(self.screen, fg, (x + self.ground_x + 22, GROUND_Y + 8, 8, 2))
        for obs in self.obstacles:
            obs.draw(self.screen)
        self.dino.draw(self.screen, dino_color)
        score_text = self.font.render(f"HI {self.high_score:05d}   {self.score:05d}", True, fg)
        self.screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 15))
        if not self.started and not self.game_over:
            msg = self.font.render("Press SPACE or UP to start  -  DOWN to duck", True, fg)
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 10))
        if self.game_over:
            over = self.big_font.render("GAME OVER", True, fg)
            self.screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 60))
            restart = self.font.render("Press SPACE to restart", True, fg)
            self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        if not self.started:
                            self.started = True
                        elif self.game_over:
                            self.reset()
                            self.started = True
                        else:
                            self.dino.jump()
                    if event.key == pygame.K_DOWN and self.started and not self.game_over:
                        self.dino.duck(True)
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.dino.duck(False)
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
