import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()
 
#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

COIN_SCORE = 0
N = 10 # Порог очков для ускорения врагов
LAST_SPEED_UP = 0 # Чтобы ускорение срабатывало один раз за порог
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("AnimatedStreet.png")
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 1. ЗАГРУЗКА ИЗОБРАЖЕНИЙ (сделай это один раз при создании объекта)
        # Убедись, что файлы 'coin_gold.png' и 'coin_silver.png' находятся в папке с игрой.
        
        # Загружаем и сразу масштабируем, чтобы монеты были аккуратными (например, 35x35 и 25x25 пикселей)
        try:
            self.gold_img = pygame.image.load("coin.png").convert_alpha()
            self.gold_img = pygame.transform.scale(self.gold_img, (35, 35))
            
            self.silver_img = pygame.image.load("silver.png").convert_alpha()
            self.silver_img = pygame.transform.scale(self.silver_img, (25, 25))
        except pygame.error:
            # Если файлов нет, создаем цветные квадраты, чтобы игра не вылетала
            print("Ошибка: Файлы монет не найдены. Используются стандартные заглушки.")
            self.gold_img = pygame.Surface((35, 35))
            self.gold_img.fill((255, 215, 0)) # Золотой цвет
            
            self.silver_img = pygame.Surface((25, 25))
            self.silver_img.fill((192, 192, 192)) # Серебряный цвет

        self.reset()

    def reset(self):
        # 2. ЛОГИКА ВЫБОРА МОНЕТЫ (остается прежней)
        # Случайно выбираем вес: 1 (серебряная) или 5 (золотая)
        self.weight = random.choices([1, 5], weights=[80, 20])[0]
        
        # 3. НАЗНАЧЕНИЕ КАРТИНКИ В ЗАВИСИМОСТИ ОТ ВЕСА
        if self.weight == 5:
            self.image = self.gold_img
        else:
            self.image = self.silver_img
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Движение монет (остается прежним)
        self.rect.move_ip(0, SPEED) 
        if self.rect.top > 600:
            self.reset()
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

COIN_SCORE = 0 # Separate counter for coin
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites.add(C1) # Adding to general group for rendering
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
 
#Game Loop
# Game Loop
while True:
    # 1. Обработка событий (Events)
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # 2. Отрисовка ФОНА (всегда ПЕРВЫМ делом)
    DISPLAYSURF.blit(background, (0,0))

    # 3. Логика монет (Collision)
    collected_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected_coins:
        COIN_SCORE += coin.weight # Добавляем вес (1 или 5)
        
        # Ускорение врагов при достижении N монет
        if COIN_SCORE // N > LAST_SPEED_UP:
            SPEED += 1.0  # Увеличиваем скорость
            LAST_SPEED_UP = COIN_SCORE // N
            print(f"Speed Increased! Current Speed: {SPEED}")
            
        pygame.mixer.Sound('coin_collect.wav').play() # Включи, если файл есть
        coin.reset()

    # 4. Движение и Отрисовка спрайтов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # 5. Отрисовка ТЕКСТА (поверх машин)
    scores = font_small.render("Enemies: " + str(SCORE), True, BLACK)
    coin_count = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_count, (SCREEN_WIDTH - 120, 10))

    # 6. Проверка столкновения с врагом (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play() # Включи, если файл есть
        time.sleep(0.5)
        
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill() 
            
        time.sleep(2)
        pygame.quit()
        sys.exit()         
         
    # 7. Обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)