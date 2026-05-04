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
CYAN = (0, 220, 220)

# Цвета машины игрока из настроек
CAR_COLORS = {
    "blue":   BLUE,
    "red":    RED,
    "green":  GREEN,
    "yellow": YELLOW,
}


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


def make_player_image(car_color_name):
    """Строим силуэт машины нужного цвета если нет спрайта."""
    color = CAR_COLORS.get(car_color_name, BLUE)
    surf = pygame.Surface((45, 70), pygame.SRCALPHA)
    # Кузов
    pygame.draw.rect(surf, color, (0, 10, 45, 50), border_radius=6)
    # Лобовое стекло
    pygame.draw.rect(surf, (180, 230, 255), (8, 14, 29, 16), border_radius=3)
    # Колёса
    pygame.draw.rect(surf, BLACK, (2, 54, 12, 14), border_radius=3)
    pygame.draw.rect(surf, BLACK, (31, 54, 12, 14), border_radius=3)
    pygame.draw.rect(surf, BLACK, (2, 4, 12, 10), border_radius=3)
    pygame.draw.rect(surf, BLACK, (31, 4, 12, 10), border_radius=3)
    return surf


# ─────────────────────────────────────────────
# Классы игровых объектов
# ─────────────────────────────────────────────

class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(200, 520))
        self.base_speed = 6
        self.speed = 6
        self.shield = False
        self.slow_until = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += self.speed

    def update(self, now):
        # Восстанавливаем скорость после замедления по таймеру
        if self.speed < self.base_speed and now >= self.slow_until:
            self.speed = self.base_speed

    def slow_down(self, now, duration=2000):
        self.speed = 3
        self.slow_until = now + duration

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.shield:
            pygame.draw.circle(screen, CYAN, self.rect.center, 38, 3)


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
        self.h_speed = 0
        self.h_dir = 1
        self.reset(player_rect)

    def reset(self, player_rect=None):
        self.kind = random.choice(["oil", "barrier", "pothole", "bump"])
        self.rect = pygame.Rect(random.choice(LANES), random.randint(-900, -120), 45, 30)

        if player_rect and abs(self.rect.centerx - player_rect.centerx) < 45:
            self.rect.y -= 300

        # Только барьер движется горизонтально
        if self.kind == "barrier":
            self.h_speed = random.choice([2, 3])
            self.h_dir = random.choice([-1, 1])
        else:
            self.h_speed = 0

    def update(self, speed, player_rect):
        self.speed = speed
        self.rect.y += self.speed

        # Движущийся барьер отражается от границ дороги
        if self.h_speed > 0:
            self.rect.x += self.h_speed * self.h_dir
            if self.rect.right >= ROAD_RIGHT or self.rect.left <= ROAD_LEFT:
                self.h_dir *= -1

        if self.rect.top > HEIGHT:
            self.reset(player_rect)

    def draw(self, screen):
        if self.kind == "oil":
            pygame.draw.ellipse(screen, BLACK, self.rect)
            pygame.draw.ellipse(screen, (40, 40, 80), self.rect.inflate(-8, -6))
        elif self.kind == "barrier":
            pygame.draw.rect(screen, ORANGE, self.rect)
            for i in range(0, self.rect.width, 10):
                pygame.draw.rect(screen, WHITE, (self.rect.x + i, self.rect.y, 5, self.rect.height))
        elif self.kind == "pothole":
            pygame.draw.ellipse(screen, DARK_GRAY, self.rect)
            pygame.draw.ellipse(screen, BLACK, self.rect.inflate(-10, -8), 2)
        else:  # bump
            pygame.draw.rect(screen, PURPLE, self.rect, border_radius=8)


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
            color = CYAN
        else:
            color = GREEN

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=6)
        draw_text(screen, self.kind[0].upper(), self.rect.x + 9, self.rect.y + 5, WHITE, 15)


class NitroStrip:
    """
    Поперечная полоса на дороге — наезд даёт кратковременный буст +2 на 3 сек.
    Мерцает жёлтым, чтобы игрок её заметил.
    """
    def __init__(self, speed):
        self.speed = speed
        self.rect = pygame.Rect(ROAD_LEFT, -60, ROAD_RIGHT - ROAD_LEFT, 18)
        self.active = False
        self.blink_timer = 0
        self._spawn()

    def _spawn(self):
        self.rect.y = random.randint(-1500, -400)
        self.active = False

    def update(self, speed):
        self.speed = speed
        self.rect.y += self.speed
        self.blink_timer += 1
        if self.rect.top > HEIGHT:
            self._spawn()

    def draw(self, screen):
        # Мерцание: видима каждые 6 кадров
        if (self.blink_timer // 6) % 2 == 0:
            pygame.draw.rect(screen, YELLOW, self.rect)
            for lx in range(ROAD_LEFT + 15, ROAD_RIGHT - 20, 45):
                pts = [
                    (lx,      self.rect.bottom - 2),
                    (lx + 10, self.rect.top + 2),
                    (lx + 20, self.rect.bottom - 2),
                ]
                pygame.draw.polygon(screen, ORANGE, pts)


# ─────────────────────────────────────────────
# Рисование дороги
# ─────────────────────────────────────────────

def draw_road(screen, background, offset):
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(GREEN)
        pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    for x in [120, 190, 260]:
        for y in range(-80, HEIGHT, 80):
            pygame.draw.rect(screen, WHITE, (x, y + offset, 5, 40))


# ─────────────────────────────────────────────
# Сохранение счёта
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
# Динамическое масштабирование сложности
# ─────────────────────────────────────────────

def get_target_counts(distance, base_enemy, base_obstacle):
    """Каждые 800м +1 враг и +1 препятствие, максимум +3 от базы."""
    bonus = min(int(distance // 800), 3)
    return base_enemy + bonus, base_obstacle + bonus


# ─────────────────────────────────────────────
# Основная игровая функция
# ─────────────────────────────────────────────

def play_game(screen, username, settings):
    clock = pygame.time.Clock()

    try:
        background = pygame.image.load(asset_path("AnimatedStreet.png")).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except Exception:
        background = None

    # Цвет машины из настроек
    car_color = settings.get("car_color", "blue")
    try:
        player_img = pygame.image.load(asset_path("Player.png")).convert_alpha()
        player_img = pygame.transform.scale(player_img, (45, 70))
    except Exception:
        player_img = make_player_image(car_color)

    enemy_img = load_image("Enemy.png", (45, 70), RED)
    coin_img = load_image("coin.png", (25, 25), YELLOW)

    try:
        crash_sound = pygame.mixer.Sound(asset_path("crash.wav"))
    except Exception:
        crash_sound = None

    difficulty = settings["difficulty"]

    if difficulty == "easy":
        base_speed = 4
        base_enemy_count = 2
        base_obstacle_count = 2
    elif difficulty == "hard":
        base_speed = 7
        base_enemy_count = 4
        base_obstacle_count = 4
    else:
        base_speed = 5
        base_enemy_count = 3
        base_obstacle_count = 3

    player = Player(player_img)
    enemies = [Enemy(enemy_img, base_speed + 1, player.rect) for _ in range(base_enemy_count)]
    coins = [Coin(coin_img, base_speed) for _ in range(3)]
    obstacles = [Obstacle(base_speed, player.rect) for _ in range(base_obstacle_count)]
    powerups = [PowerUp(base_speed)]
    nitro_strip = NitroStrip(base_speed)

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

        # ── Конец нитро-буста ──
        if active_power == "nitro" and now > power_end_time:
            active_power = None
            speed_bonus = 0

        game_speed = base_speed + speed_bonus + int(distance // 800)

        # ── Динамическое масштабирование: добавляем объекты по ходу игры ──
        target_enemies, target_obstacles = get_target_counts(
            distance, base_enemy_count, base_obstacle_count
        )
        while len(enemies) < target_enemies:
            enemies.append(Enemy(enemy_img, game_speed + 1, player.rect))
        while len(obstacles) < target_obstacles:
            obstacles.append(Obstacle(game_speed, player.rect))

        # ── Обновление дороги ──
        road_offset = (road_offset + game_speed) % 80
        distance += game_speed * 0.12
        score = int(distance + coins_collected * 10)

        draw_road(screen, background, road_offset)

        # ── Нитро-полоса на дороге ──
        nitro_strip.update(game_speed)
        nitro_strip.draw(screen)

        if player.rect.colliderect(nitro_strip.rect) and not nitro_strip.active:
            nitro_strip.active = True
            if active_power is None:
                active_power = "nitro"
                speed_bonus = 2
                power_end_time = now + 3000

        # ── Игрок ──
        player.move()
        player.update(now)

        # ── Враги ──
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

        # ── Препятствия ──
        for obstacle in obstacles:
            obstacle.update(game_speed, player.rect)
            obstacle.draw(screen)

            if player.rect.colliderect(obstacle.rect):
                if player.shield:
                    player.shield = False
                    active_power = None
                    obstacle.reset(player.rect)
                elif obstacle.kind in ["oil", "bump"]:
                    player.slow_down(now, duration=2000)
                    obstacle.reset(player.rect)
                else:
                    if settings["sound"] and crash_sound:
                        crash_sound.play()
                    save_score(username, score, int(distance), coins_collected)
                    return "game_over", score, int(distance), coins_collected

        # ── Монеты ──
        for coin in coins:
            coin.update(game_speed)
            coin.draw(screen)
            if player.rect.colliderect(coin.rect):
                coins_collected += coin.value
                coin.reset()

        # ── Пауэрапы ──
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

        # ── HUD ──
        remaining = max(0, finish_distance - int(distance))
        draw_text(screen, f"Name: {username}",         10,  10, WHITE, 14)
        draw_text(screen, f"Score: {score}",           10,  30, WHITE, 14)
        draw_text(screen, f"Coins: {coins_collected}",  10,  50, WHITE, 14)
        draw_text(screen, f"Distance: {int(distance)}m", 210, 10, WHITE, 14)
        draw_text(screen, f"Remain: {remaining}m",     210, 30, WHITE, 14)

        if active_power == "nitro":
            left = max(0, (power_end_time - now) // 1000)
            draw_text(screen, f"Power: Nitro {left}s", 210, 50, YELLOW, 14)
        elif player.shield:
            draw_text(screen, "Power: Shield", 210, 50, CYAN, 14)
        else:
            draw_text(screen, "Power: None", 210, 50, WHITE, 14)

        # ── Финиш ──
        if distance >= finish_distance:
            score += 1000
            save_score(username, score, int(distance), coins_collected)
            return "victory", score, int(distance), coins_collected

        pygame.display.update()