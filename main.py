import pygame
import random
pygame.init()

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
icon_image = pygame.image.load("./images/Icon.png")
pygame.display.set_icon(icon_image)

BACKGROUND = pygame.transform.scale(pygame.image.load("./images/background-black.png"), (WIDTH, HEIGHT))

PLAYER_SHIP = pygame.transform.scale(pygame.image.load("./images/player_ship.png"), (100, 90))
PLAYER_LASER = pygame.image.load("./images/laser_blue.png")

RED_ENEMY = pygame.transform.scale(pygame.image.load("./images/spaceship_red.png"), (70, 50))
YELLOW_ENEMY = pygame.transform.scale(pygame.image.load("./images/spaceship_yellow.png"), (70, 50))
RED_LASER = pygame.image.load("./images/laser_red.png")
YELLOW_LASER = pygame.image.load("./images/laser_yellow.png")


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, laser_val):
        self.y -= laser_val

    def oof_screen(self):
        return self.y >= HEIGHT or self.y <= 0


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_count = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def cooldown(self):
        if self.cool_down_count >= self.COOLDOWN:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    def move_lasers(self, laser_val):
        self.cooldown()
        for laser in self.lasers:
            laser.move(laser_val)

    def shoot(self):
        if self.cool_down_count == 0:
            newLaser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(newLaser)
            self.cool_down_count = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ship_img, self.laser_img = PLAYER_SHIP, PLAYER_LASER
        self.health, self.max_health = 100, 100


class Enemy(Ship):
    ENEMY_DICT = {
        "red": (RED_ENEMY, RED_LASER),
        "yellow": (YELLOW_ENEMY, YELLOW_LASER)
    }

    def __init__(self, x, y, color):
        super().__init__(x, y)
        self.ship_img, self.laser_img = self.ENEMY_DICT[color]

    def move(self, enemy_val):
        self.y += enemy_val


def main():
    running = True
    lost = False
    FPS = 60
    clock = pygame.time.Clock()

    lost_count = 0

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    lives = 5
    level = 0

    player = Player(330, 650)
    player_val = 5

    enemies = []
    enemy_val = 4
    wave_len = 0
    enemy_increase = 5

    laser_val = 7

    def re_draw():
        WINDOW.blit(BACKGROUND, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        if lost:
            lost_label = lost_font.render("You lost!", True, (255, 255, 255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,
                                     HEIGHT/2 - lost_label.get_height()/2))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        pygame.display.update()

    while running:
        clock.tick(FPS)
        re_draw()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                running = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_len += enemy_increase
            for i in range(wave_len):
                newX = random.randrange(0, WIDTH - 70 - 10)
                newY = random.randrange(-1500, -100)
                newColor = random.choice(["red", "yellow"])
                newEnemy = Enemy(newX, newY, newColor)
                enemies.append(newEnemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_val > 0:
            player.x -= player_val
        if keys[pygame.K_d] and player.x + player_val + player.get_width() < WIDTH:
            player.x += player_val
        if keys[pygame.K_w] and player.y - player_val > 0:
            player.y -= player_val
        if keys[pygame.K_s] and player.y + player_val + player.get_height() < HEIGHT:
            player.y += player_val
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_val)
            enemy.move_lasers(-laser_val)

            if random.randrange(0, 3*60) == 1:
                enemy.shoot()

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(laser_val)


main()
