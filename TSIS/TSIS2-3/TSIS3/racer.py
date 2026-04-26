import pygame
import random
import os
from datetime import datetime
from persistence import load_leaderboard, save_leaderboard
from ui import draw_text

WIDTH = 400
HEIGHT = 600
FPS = 60

ROAD_LEFT = 40
ROAD_RIGHT = 360
LANES = [80, 150, 220, 290]

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (60, 60, 60)
GREEN = (40, 180, 80)
RED = (220, 40, 40)
BLUE = (40, 100, 220)
YELLOW = (240, 210, 40)
ORANGE = (255, 140, 0)
PURPLE = (160, 80, 220)


def asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)


def load_image(filename, size, fallback_color):
    try:
        img = pygame.image.load(asset_path(filename)).convert_alpha()
        return pygame.transform.scale(img, size)
    except Exception:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf


class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(200, 520))
        self.speed = 6
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.shield:
            pygame.draw.circle(screen, BLUE, self.rect.center, 38, 3)


class Enemy:
    def __init__(self, image, speed, player_rect=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset(player_rect)

    def reset(self, player_rect=None):
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-700, -80)

        if player_rect and abs(self.rect.centerx - player_rect.centerx) < 45:
            self.rect.y -= 300

    def update(self, speed, player_rect):
        self.speed = speed
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset(player_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Coin:
    def __init__(self, image, speed):
        self.base_image = image
        self.speed = speed
        self.reset()

    def reset(self):
        self.value = random.choice([1, 2, 5, 10])
        size = 20 + self.value * 2
        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = random.randint(-700, -100)

    def update(self, speed):
        self.speed = speed
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, speed, player_rect=None):
        self.speed = speed
        self.reset(player_rect)

    def reset(self, player_rect=None):
        self.kind = random.choice(["oil", "barrier", "pothole", "bump"])
        self.rect = pygame.Rect(random.choice(LANES), random.randint(-900, -120), 45, 30)

        if player_rect and abs(self.rect.centerx - player_rect.centerx) < 45:
            self.rect.y -= 300

    def update(self, speed, player_rect):
        self.speed = speed
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset(player_rect)

    def draw(self, screen):
        if self.kind == "oil":
            color = BLACK
        elif self.kind == "barrier":
            color = ORANGE
        elif self.kind == "pothole":
            color = DARK_GRAY
        else:
            color = PURPLE

        pygame.draw.rect(screen, color, self.rect)


class PowerUp:
    def __init__(self, speed):
        self.speed = speed
        self.reset()

    def reset(self):
        self.kind = random.choice(["nitro", "shield", "repair"])
        self.rect = pygame.Rect(random.choice(LANES), random.randint(-1200, -250), 30, 30)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, speed):
        self.speed = speed
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset()

        if pygame.time.get_ticks() - self.spawn_time > 8000:
            self.reset()

    def draw(self, screen):
        if self.kind == "nitro":
            color = ORANGE
        elif self.kind == "shield":
            color = BLUE
        else:
            color = GREEN

        pygame.draw.rect(screen, color, self.rect)
        draw_text(screen, self.kind[0].upper(), self.rect.x + 7, self.rect.y + 3, WHITE, 15)


def draw_road(screen, background, offset):
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    for x in [120, 190, 260]:
        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (x, y + offset, 5, 40))


def save_score(username, score, distance, coins):
    data = load_leaderboard()
    data.append({
        "name": username,
        "score": score,
        "distance": distance,
        "coins": coins,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_leaderboard(data)


def play_game(screen, username, settings):
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load(asset_path("AnimatedStreet.png")).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception:
        background = None

    player_img = load_image("Player.png", (45, 70), BLUE)
    enemy_img = load_image("Enemy.png", (45, 70), RED)
    coin_img = load_image("coin.png", (25, 25), YELLOW)

    try:
        crash_sound = pygame.mixer.Sound(asset_path("crash.wav"))
    except Exception:
        crash_sound = None

    difficulty = settings["difficulty"]

    if difficulty == "easy":
        base_speed = 4
        enemy_count = 2
        obstacle_count = 2
    elif difficulty == "hard":
        base_speed = 7
        enemy_count = 4
        obstacle_count = 4
    else:
        base_speed = 5
        enemy_count = 3
        obstacle_count = 3

    player = Player(player_img)

    enemies = [Enemy(enemy_img, base_speed + 1, player.rect) for _ in range(enemy_count)]
    coins = [Coin(coin_img, base_speed) for _ in range(3)]
    obstacles = [Obstacle(base_speed, player.rect) for _ in range(obstacle_count)]
    powerups = [PowerUp(base_speed)]

    coins_collected = 0
    distance = 0
    finish_distance = 3000
    score = 0

    road_offset = 0
    active_power = None
    power_end_time = 0
    speed_bonus = 0

    while True:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, int(distance), coins_collected

        if active_power == "nitro" and now > power_end_time:
            active_power = None
            speed_bonus = 0

        game_speed = base_speed + speed_bonus + int(distance // 800)

        road_offset = (road_offset + game_speed) % 80
        distance += game_speed * 0.12
        score = int(distance + coins_collected * 10)

        draw_road(screen, background, road_offset)

        player.move()

        for enemy in enemies:
            enemy.update(game_speed + 1, player.rect)
            enemy.draw(screen)

            if player.rect.colliderect(enemy.rect):
                if player.shield:
                    player.shield = False
                    active_power = None
                    enemy.reset(player.rect)
                else:
                    if settings["sound"] and crash_sound:
                        crash_sound.play()
                    save_score(username, score, int(distance), coins_collected)
                    return "game_over", score, int(distance), coins_collected

        for obstacle in obstacles:
            obstacle.update(game_speed, player.rect)
            obstacle.draw(screen)

            if player.rect.colliderect(obstacle.rect):
                if player.shield:
                    player.shield = False
                    active_power = None
                    obstacle.reset(player.rect)
                elif obstacle.kind in ["oil", "bump"]:
                    player.speed = 3
                else:
                    if settings["sound"] and crash_sound:
                        crash_sound.play()
                    save_score(username, score, int(distance), coins_collected)
                    return "game_over", score, int(distance), coins_collected

        player.speed = 6

        for coin in coins:
            coin.update(game_speed)
            coin.draw(screen)

            if player.rect.colliderect(coin.rect):
                coins_collected += coin.value
                coin.reset()

        for powerup in powerups:
            powerup.update(game_speed)
            powerup.draw(screen)

            if player.rect.colliderect(powerup.rect):
                if active_power is None:
                    if powerup.kind == "nitro":
                        active_power = "nitro"
                        speed_bonus = 4
                        power_end_time = now + 4000

                    elif powerup.kind == "shield":
                        active_power = "shield"
                        player.shield = True

                    elif powerup.kind == "repair":
                        if obstacles:
                            obstacles[0].reset(player.rect)
                        score += 50

                powerup.reset()

        player.draw(screen)

        remaining = max(0, finish_distance - int(distance))

        draw_text(screen, f"Name: {username}", 10, 10, WHITE, 14)
        draw_text(screen, f"Score: {score}", 10, 30, WHITE, 14)
        draw_text(screen, f"Coins: {coins_collected}", 10, 50, WHITE, 14)
        draw_text(screen, f"Distance: {int(distance)}m", 210, 10, WHITE, 14)
        draw_text(screen, f"Remain: {remaining}m", 210, 30, WHITE, 14)

        if active_power == "nitro":
            left = max(0, (power_end_time - now) // 1000)
            draw_text(screen, f"Power: Nitro {left}s", 210, 50, WHITE, 14)
        elif player.shield:
            draw_text(screen, "Power: Shield", 210, 50, WHITE, 14)
        else:
            draw_text(screen, "Power: None", 210, 50, WHITE, 14)

        if distance >= finish_distance:
            score += 1000
            save_score(username, score, int(distance), coins_collected)
            return "game_over", score, int(distance), coins_collected

        pygame.display.update()