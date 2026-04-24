import pygame
import random
import sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

pygame.init()


WIDTH, HEIGHT = 600, 600
CELL = 30
FPS_INITIAL = 5 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Level System")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 20)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        # Moving tail with body
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def check_collision(self):

        


        head = self.body[0]
        # Checking for colliding with walls 
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        # Checking for colliding with itself
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False
    

    def draw(self):
        for i, segment in enumerate(self.body):
            color = RED if i == 0 else YELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL - 1, CELL - 1))

class Food:
    def __init__(self):
        self.pos = Point(0, 0)
        self.weight = 1
        self.color = GREEN
        self.spawn_time = 0  # Eating time
        self.lifetime = 5000  # Time of living in milliseconds 
        self.generate_random_pos([])

    def generate_random_pos(self, snake_body):
        self.weight = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        if self.weight == 1: self.color = GREEN
        elif self.weight == 2: self.color = YELLOW
        elif self.weight == 3: self.color = (128, 0, 128)

        # Remembering current time while creating new food
        self.spawn_time = pygame.time.get_ticks()

        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            on_snake = any(seg.x == self.pos.x and seg.y == self.pos.y for seg in snake_body)
            if not on_snake:
                break

    def is_expired(self):
        # Checking, whether time goes over 5 sec 
        current_time = pygame.time.get_ticks()
        return current_time - self.spawn_time > self.lifetime

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL - 1, CELL - 1))

# Initializating objects
snake = Snake()
food = Food()
food.generate_random_pos(snake.body)

score = 0
level = 1
speed = FPS_INITIAL
running = True

while running:
    # Processing events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    # Moving
    snake.move()

    # Checking for craching
    if snake.check_collision():
        print(f"Game Over! Score: {score}")
        running = False

    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        added_weight = food.weight
        score += added_weight
        
        # Растем на столько сегментов, сколько весит еда
        for _ in range(added_weight):
            snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))
        
        # Generating new food
        food.generate_random_pos(snake.body)
        
        # Updating level every 5 point
        new_level = (score // 5) + 1
        if new_level > level:
            level = new_level
            speed += 1 
    if food.is_expired():
        food.generate_random_pos(snake.body)

    # Checking for eating a food
    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        food.generate_random_pos(snake.body)        

    # Drawing
    screen.fill(BLACK)
    
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    snake.draw()
    food.draw()

    score_text = font_small.render(f"Score: {score}", True, WHITE)
    level_text = font_small.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
