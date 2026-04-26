import pygame
import random
import json
import os
import sys
from db import get_personal_best, save_game_result

WIDTH = 800
HEIGHT = 600
CELL = 40

FOOD_LIFETIME = 7000
POWERUP_LIFETIME = 8000
POWERUP_DURATION = 5000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_RED = (120, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)
YELLOW = (240, 220, 0)
PURPLE = (160, 0, 200)
GRAY = (90, 90, 90)

BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default = {
            "snake_color": [0, 200, 0],
            "grid": True,
            "sound": True
        }
        save_settings(default)
        return default

    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def load_image(path, size, fallback_color):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except Exception:
        surface = pygame.Surface(size)
        surface.fill(fallback_color)
        return surface


class SnakeGame:
    def __init__(self, screen, username):
        self.screen = screen
        self.username = username
        self.clock = pygame.time.Clock()

        self.settings = load_settings()
        self.personal_best = get_personal_best(username)

        self.font = pygame.font.SysFont("Verdana", 24)
        self.small_font = pygame.font.SysFont("Verdana", 18)

        self.background_img = load_image(
            os.path.join(BASE_DIR, "assets", "images", "background.png"),
            (WIDTH, HEIGHT),
            BLACK
        )

        self.head_img = load_image(
            os.path.join(BASE_DIR, "assets", "images", "head.png"),
            (CELL, CELL),
            GREEN
        )

        self.body_img = load_image(
            os.path.join(BASE_DIR, "assets", "images", "body.png"),
            (CELL, CELL),
            GREEN
        )

        self.food_img = load_image(
            os.path.join(BASE_DIR, "assets", "images", "food.png"),
            (CELL, CELL),
            RED
        )

        self.reset()

    def reset(self):
        self.snake = [
            [200, 200],
            [160, 200],
            [120, 200]
        ]

        self.dx = CELL
        self.dy = 0

        self.score = 0
        self.level = 1
        self.speed = 10

        self.obstacles = []
        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.food = None
        self.poison = None
        self.powerup = None
        self.powerup_spawn_time = 0

        self.food = self.generate_food()
        self.poison = self.generate_poison()

    def all_blocked_positions(self):
        blocked = []

        blocked.extend(self.snake)
        blocked.extend(self.obstacles)

        if hasattr(self, "food") and self.food:
            blocked.append([self.food["x"], self.food["y"]])

        if hasattr(self, "poison") and self.poison:
            blocked.append([self.poison["x"], self.poison["y"]])

        if hasattr(self, "powerup") and self.powerup:
            blocked.append([self.powerup["x"], self.powerup["y"]])

        return blocked

    def random_cell(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            if [x, y] not in self.all_blocked_positions():
                return x, y

    def generate_food(self):
        x, y = self.random_cell()

        return {
            "x": x,
            "y": y,
            "value": random.choice([1, 3, 5, 10]),
            "spawn_time": pygame.time.get_ticks()
        }

    def generate_poison(self):
        x, y = self.random_cell()

        return {
            "x": x,
            "y": y,
            "spawn_time": pygame.time.get_ticks()
        }

    def generate_powerup(self):
        x, y = self.random_cell()

        self.powerup_spawn_time = pygame.time.get_ticks()

        return {
            "x": x,
            "y": y,
            "kind": random.choice(["speed", "slow", "shield"])
        }

    def generate_obstacles(self):
        if self.level < 3:
            return

        self.obstacles = []

        count = self.level + 1
        head = self.snake[0]

        attempts = 0

        while len(self.obstacles) < count and attempts < 200:
            attempts += 1

            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)

            pos = [x, y]

            too_close = abs(x - head[0]) <= CELL * 2 and abs(y - head[1]) <= CELL * 2

            if pos not in self.snake and pos not in self.obstacles and not too_close:
                self.obstacles.append(pos)

    def update_level(self):
        old_level = self.level

        self.level = self.score // 5 + 1

        if self.level != old_level:
            self.generate_obstacles()

        self.speed = 10 + (self.level - 1) * 2

        if self.active_power == "speed":
            self.speed += 5
        elif self.active_power == "slow":
            self.speed = max(5, self.speed - 5)

    def handle_power_timer(self):
        now = pygame.time.get_ticks()

        if self.active_power in ["speed", "slow"] and now > self.power_end_time:
            self.active_power = None

        if self.powerup is None:
            if random.randint(1, 250) == 1:
                self.powerup = self.generate_powerup()
        else:
            if now - self.powerup_spawn_time > POWERUP_LIFETIME:
                self.powerup = None

    def collision_game_over(self):
        if self.shield:
            self.shield = False
            self.active_power = None
            return False

        return True

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = [head_x + self.dx, head_y + self.dy]

        border_collision = (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        )

        if border_collision:
            if self.collision_game_over():
                return False
            new_head = self.snake[0]

        ate_food = (
            new_head[0] == self.food["x"] and
            new_head[1] == self.food["y"]
        )

        ate_poison = (
            new_head[0] == self.poison["x"] and
            new_head[1] == self.poison["y"]
        )

        hit_powerup = (
            self.powerup is not None and
            new_head[0] == self.powerup["x"] and
            new_head[1] == self.powerup["y"]
        )

        if new_head in self.obstacles:
            if self.collision_game_over():
                return False

        if ate_food:
            if new_head in self.snake:
                if self.collision_game_over():
                    return False
        else:
            if new_head in self.snake[:-1]:
                if self.collision_game_over():
                    return False

        self.snake.insert(0, new_head)

        if ate_food:
            self.score += self.food["value"]
            self.food = self.generate_food()
        else:
            self.snake.pop()

        if ate_poison:
            if len(self.snake) <= 3:
                return False

            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()

            self.poison = self.generate_poison()

        if hit_powerup:
            kind = self.powerup["kind"]

            if kind == "speed":
                self.active_power = "speed"
                self.power_end_time = pygame.time.get_ticks() + POWERUP_DURATION

            elif kind == "slow":
                self.active_power = "slow"
                self.power_end_time = pygame.time.get_ticks() + POWERUP_DURATION

            elif kind == "shield":
                self.active_power = "shield"
                self.shield = True

            self.powerup = None

        return True

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y), 1)

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))

        self.draw_grid()

        for block in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (block[0], block[1], CELL, CELL))

        for i, segment in enumerate(self.snake):
            if i == 0:
                self.screen.blit(self.head_img, (segment[0], segment[1]))
            else:
                self.screen.blit(self.body_img, (segment[0], segment[1]))

        food_age = pygame.time.get_ticks() - self.food["spawn_time"]

        if food_age > FOOD_LIFETIME:
            self.food = self.generate_food()
        else:
            life_ratio = max(0.5, 1 - food_age / FOOD_LIFETIME)
            size = int(CELL * 1.3 * life_ratio)
            scaled_food = pygame.transform.scale(self.food_img, (size, size))

            draw_x = self.food["x"] - (size - CELL) // 2
            draw_y = self.food["y"] - (size - CELL) // 2

            self.screen.blit(scaled_food, (draw_x, draw_y))

        pygame.draw.rect(
            self.screen,
            DARK_RED,
            (self.poison["x"], self.poison["y"], CELL, CELL)
        )

        if self.powerup:
            if self.powerup["kind"] == "speed":
                color = YELLOW
                label = "S"
            elif self.powerup["kind"] == "slow":
                color = BLUE
                label = "L"
            else:
                color = PURPLE
                label = "H"

            pygame.draw.rect(
                self.screen,
                color,
                (self.powerup["x"], self.powerup["y"], CELL, CELL)
            )

            text = self.small_font.render(label, True, WHITE)
            self.screen.blit(text, (self.powerup["x"] + 12, self.powerup["y"] + 8))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        best_text = self.font.render(f"Best: {self.personal_best}", True, WHITE)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(best_text, (10, 70))

        if self.active_power:
            power_text = self.small_font.render(f"Power: {self.active_power}", True, WHITE)
            self.screen.blit(power_text, (600, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.dx == 0:
                        self.dx = -CELL
                        self.dy = 0
                    elif event.key == pygame.K_RIGHT and self.dx == 0:
                        self.dx = CELL
                        self.dy = 0
                    elif event.key == pygame.K_UP and self.dy == 0:
                        self.dx = 0
                        self.dy = -CELL
                    elif event.key == pygame.K_DOWN and self.dy == 0:
                        self.dx = 0
                        self.dy = CELL

            self.handle_power_timer()

            alive = self.move_snake()

            self.update_level()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.speed)

            if not alive:
                save_game_result(self.username, self.score, self.level)
                return self.score, self.level, self.personal_best