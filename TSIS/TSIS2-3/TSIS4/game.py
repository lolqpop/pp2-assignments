import pygame, random, json, os, sys
from db import get_personal_best, save_game_result

WIDTH, HEIGHT, CELL = 800, 600, 40
FOOD_LIFETIME, POWERUP_LIFETIME, POWERUP_DURATION = 7000, 8000, 5000

WHITE=(255,255,255); BLACK=(0,0,0); RED=(200,0,0); DARK_RED=(120,0,0)
GREEN=(0,200,0); BLUE=(0,100,255); YELLOW=(240,220,0); PURPLE=(160,0,200); GRAY=(90,90,90)

BASE_DIR = os.path.dirname(__file__)
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default = {"snake_color":[0,200,0],"grid":True,"sound":True}
        save_settings(default); return default
    with open(SETTINGS_FILE) as f: return json.load(f)

def save_settings(s):
    with open(SETTINGS_FILE,"w") as f: json.dump(s,f,indent=4)

def load_image(path, size, fallback):
    try: return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
    except:
        s = pygame.Surface(size); s.fill(fallback); return s


class SnakeGame:
    def __init__(self, screen, username):
        self.screen, self.username = screen, username
        self.clock = pygame.time.Clock()
        self.settings = load_settings()
        self.personal_best = get_personal_best(username)
        self.font = pygame.font.SysFont("Verdana", 24)
        self.small_font = pygame.font.SysFont("Verdana", 18)

        img = lambda n, fb: load_image(os.path.join(BASE_DIR,"assets","images",n),(CELL,CELL),fb)
        sc = tuple(self.settings["snake_color"])

        self.bg_img   = load_image(os.path.join(BASE_DIR,"assets","images","background.png"),(WIDTH,HEIGHT),BLACK)
        self.head_img = img("head.png", sc)   # цвет из настроек
        self.body_img = img("body.png", sc)   # цвет из настроек
        self.food_img = img("food.png", RED)
        self.reset()

    def reset(self):
        self.snake = [[200,200],[160,200],[120,200]]
        self.dx, self.dy = CELL, 0
        self.score, self.level, self.speed = 0, 1, 10 #начальная скорость
        self.obstacles = []
        self.active_power, self.power_end_time, self.shield = None, 0, False
        self.powerup, self.powerup_spawn_time = None, 0
        self.generate_obstacles()           # фикс: генерируем сразу
        self.food   = self.gen_food()
        self.poison = self.gen_poison()

    def all_blocked(self):
        b = list(self.snake) + list(self.obstacles)
        for a in ("food","poison","powerup"):
            o = getattr(self,a,None)
            if o: b.append([o["x"],o["y"]])
        return b

    def random_cell(self):
        blocked = self.all_blocked()
        while True:
            x,y = random.randrange(0,WIDTH,CELL), random.randrange(0,HEIGHT,CELL)
            if [x,y] not in blocked: return x,y

    def gen_food(self):
        x,y = self.random_cell()
        return {"x":x,"y":y,"value":random.choice([1,3,5,10]),"spawn_time":pygame.time.get_ticks()}

    def gen_poison(self):
        x,y = self.random_cell()
        return {"x":x,"y":y,"spawn_time":pygame.time.get_ticks()}

    def gen_powerup(self):
        x,y = self.random_cell()
        self.powerup_spawn_time = pygame.time.get_ticks()
        return {"x":x,"y":y,"kind":random.choice(["speed","slow","shield"])}

    def generate_obstacles(self):
        if self.level < 3: return
        self.obstacles = []
        head = self.snake[0]
        attempts = 0
        while len(self.obstacles) < self.level+1 and attempts < 200:
            attempts += 1
            x,y = random.randrange(0,WIDTH,CELL), random.randrange(0,HEIGHT,CELL)
            if [x,y] not in self.snake and [x,y] not in self.obstacles and not (abs(x-head[0])<=CELL*2 and abs(y-head[1])<=CELL*2):
                self.obstacles.append([x,y])

    def update_level(self):
        old = self.level
        self.level = self.score//5+1
        if self.level != old: self.generate_obstacles()
        self.speed = 10 + (self.level - 1) * 1  #увеличение скорости
        if self.active_power=="speed": self.speed+=5
        elif self.active_power=="slow": self.speed=max(5,self.speed-5)

    def handle_power_timer(self):
        now = pygame.time.get_ticks()
        if self.active_power in ("speed","slow") and now>self.power_end_time:
            self.active_power = None
        if self.powerup is None:
            if random.randint(1,250)==1: self.powerup = self.gen_powerup()
        elif now-self.powerup_spawn_time > POWERUP_LIFETIME:
            self.powerup = None

    def use_shield(self):
        self.shield = False; self.active_power = None; return False

    def move_snake(self):
        hx,hy = self.snake[0]
        nx,ny = hx+self.dx, hy+self.dy

        # Граница — фикс: оборачиваем на другую сторону при щите
        if nx<0 or nx>=WIDTH or ny<0 or ny>=HEIGHT:
            if self.shield:
                nx,ny = nx%WIDTH, ny%HEIGHT
                return self.use_shield()
            return False

        new_head = [nx,ny]

        if new_head in self.obstacles:
            return self.use_shield() if self.shield else False

        ate   = new_head[0]==self.food["x"]   and new_head[1]==self.food["y"]
        poisd = new_head[0]==self.poison["x"] and new_head[1]==self.poison["y"]
        pwrup = self.powerup and new_head[0]==self.powerup["x"] and new_head[1]==self.powerup["y"]

        if new_head in (self.snake if ate else self.snake[:-1]):
            return self.use_shield() if self.shield else False

        self.snake.insert(0, new_head)

        if ate:
            self.score += self.food["value"]; self.food = self.gen_food()
        else:
            self.snake.pop()

        if poisd:
            if len(self.snake)<=3: return False
            for _ in range(2):
                if len(self.snake)>1: self.snake.pop()
            self.poison = self.gen_poison()

        if pwrup:
            k = self.powerup["kind"]
            if k=="shield": self.active_power,self.shield = "shield",True
            else: self.active_power,self.power_end_time = k, pygame.time.get_ticks()+POWERUP_DURATION
            self.powerup = None

        return True

    def draw_grid(self):
        if not self.settings["grid"]: return
        for x in range(0,WIDTH,CELL): pygame.draw.line(self.screen,GRAY,(x,0),(x,HEIGHT),1)
        for y in range(0,HEIGHT,CELL): pygame.draw.line(self.screen,GRAY,(0,y),(WIDTH,y),1)

    def draw(self):
        self.screen.blit(self.bg_img,(0,0))
        self.draw_grid()

        for b in self.obstacles:
            pygame.draw.rect(self.screen,GRAY,(b[0],b[1],CELL,CELL))

        for i,seg in enumerate(self.snake):
            self.screen.blit(self.head_img if i==0 else self.body_img,(seg[0],seg[1]))

        age = pygame.time.get_ticks()-self.food["spawn_time"]
        if age > FOOD_LIFETIME:
            self.food = self.gen_food()
        else:
            ratio = max(0.5, 1-age/FOOD_LIFETIME)
            size = int(CELL*1.3*ratio)
            scaled = pygame.transform.scale(self.food_img,(size,size))
            self.screen.blit(scaled,(self.food["x"]-(size-CELL)//2, self.food["y"]-(size-CELL)//2))

        pygame.draw.rect(self.screen,DARK_RED,(self.poison["x"],self.poison["y"],CELL,CELL))

        if self.powerup:
            col   = {"speed":YELLOW,"slow":BLUE,"shield":PURPLE}[self.powerup["kind"]]
            label = self.powerup["kind"][0].upper()
            pygame.draw.rect(self.screen,col,(self.powerup["x"],self.powerup["y"],CELL,CELL))
            self.screen.blit(self.small_font.render(label,True,WHITE),(self.powerup["x"]+12,self.powerup["y"]+8))

        for text,y in [(f"Score: {self.score}",10),(f"Level: {self.level}",40),(f"Best: {self.personal_best}",70)]:
            self.screen.blit(self.font.render(text,True,WHITE),(10,y))

        if self.active_power:
            self.screen.blit(self.small_font.render(f"Power: {self.active_power}",True,WHITE),(600,10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: pygame.quit(); sys.exit()
                if event.type==pygame.KEYDOWN:
                    if   event.key==pygame.K_LEFT  and self.dx==0: self.dx,self.dy=-CELL,0
                    elif event.key==pygame.K_RIGHT and self.dx==0: self.dx,self.dy= CELL,0
                    elif event.key==pygame.K_UP    and self.dy==0: self.dx,self.dy=0,-CELL
                    elif event.key==pygame.K_DOWN  and self.dy==0: self.dx,self.dy=0, CELL

            self.handle_power_timer()
            if not self.move_snake():
                save_game_result(self.username, self.score, self.level)
                return self.score, self.level, self.personal_best
            self.update_level()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.speed)