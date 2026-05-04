import pygame
import datetime
from tools import flood_fill

pygame.init()

WIDTH, HEIGHT = 1000, 800
TOOLBAR_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (200,200,200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint ")

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont("Arial", 18)
font_big = pygame.font.SysFont("Arial", 24)

tool = "pencil"
color = BLACK
size = 2

drawing = False
start_pos = (0,0)
last_pos = (0,0)

typing = False
text = ""
text_pos = (0,0)

tools_list = ["pencil","line","rect","circle","square","triangle","rhombus","fill","text","eraser"]
colors = [BLACK, RED, GREEN, BLUE]

def draw_ui():
    pygame.draw.rect(screen, (230,230,230), (0,0,WIDTH,TOOLBAR_HEIGHT))

    for i, t in enumerate(tools_list):
        rect = pygame.Rect(10 + i*95, 10, 90, 30)  
        pygame.draw.rect(screen, GRAY if tool==t else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        screen.blit(font.render(t, True, BLACK), (rect.x+5, rect.y+5))

    for i, s in enumerate([2,5,10]):
        rect = pygame.Rect(10 + i*50, 55, 40, 40)
        pygame.draw.rect(screen, GRAY if size==s else WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        pygame.draw.circle(screen, BLACK, rect.center, s)

    for i, c in enumerate(colors):
        rect = pygame.Rect(400 + i*60, 55, 40, 40)  
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    pygame.draw.rect(screen, color, (900, 30, 60, 40))
    pygame.draw.rect(screen, BLACK, (900, 30, 60, 40), 2)

def draw_shape(surf, tool, color, start, end, size):
    x1,y1 = start
    x2,y2 = end
    dx,dy = x2-x1, y2-y1

    if tool == "line":
        pygame.draw.line(surf,color,start,end,size)

    elif tool == "rect":
        pygame.draw.rect(surf,color,(min(x1,x2),min(y1,y2),abs(dx),abs(dy)),size)

    elif tool == "circle":
        r = int((dx**2+dy**2)**0.5)
        pygame.draw.circle(surf,color,start,r,size)

    elif tool == "square":
        s = max(abs(dx),abs(dy))
        sx = -s if dx < 0 else s
        sy = -s if dy < 0 else s
        pygame.draw.rect(surf,color,(min(x1,x1+sx),min(y1,y1+sy),s,s),size)

    elif tool == "triangle":
        pygame.draw.polygon(surf,color,[start,(x1,y2),end],size)

    elif tool == "rhombus":
        cx,cy = (x1+x2)//2,(y1+y2)//2
        pts = [(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
        pygame.draw.polygon(surf,color,pts,size)

running = True

while running:
    screen.fill(WHITE)
    screen.blit(canvas,(0,TOOLBAR_HEIGHT))
    draw_ui()

    mouse = pygame.mouse.get_pos()
    adj_mouse = (mouse[0], mouse[1]-TOOLBAR_HEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[1] < TOOLBAR_HEIGHT:
                # выбор инструмента
                for i,t in enumerate(tools_list):
                    if 10+i*95 <= mouse[0] <= 100+i*95 and 10<=mouse[1]<=40:
                        tool = t

                # размер
                for i,s in enumerate([2,5,10]):
                    if 10+i*50 <= mouse[0] <= 50+i*50 and 55<=mouse[1]<=95:
                        size = s

                # цвет
                for i, c in enumerate(colors):
                    if 400 + i*60 <= mouse[0] <= 440 + i*60 and 55 <= mouse[1] <= 95:
                       color = c

            else:
                if tool == "fill":
                    flood_fill(canvas, adj_mouse[0], adj_mouse[1], color)

                elif tool == "text":
                    typing = True
                    text = ""
                    text_pos = adj_mouse

                else:
                    drawing = True
                    start_pos = adj_mouse
                    last_pos = adj_mouse

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.line(canvas,color,last_pos,adj_mouse,size)
                last_pos = adj_mouse

            elif tool == "eraser":
                pygame.draw.line(canvas,WHITE,last_pos,adj_mouse,size)
                last_pos = adj_mouse

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool not in ["pencil","eraser"]:
                draw_shape(canvas,tool,color,start_pos,adj_mouse,size)
            drawing = False

        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    txt = font_big.render(text, True, color)
                    canvas.blit(txt, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

            else:
                if event.key == pygame.K_1: size = 2
                if event.key == pygame.K_2: size = 5
                if event.key == pygame.K_3: size = 10

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    name = f"paint_{datetime.datetime.now().strftime('%H%M%S')}.png"
                    pygame.image.save(canvas,name)

    # preview
    if drawing and tool not in ["pencil","eraser"]:
        preview_start = (start_pos[0], start_pos[1]+TOOLBAR_HEIGHT)
        draw_shape(screen,tool,color,preview_start,mouse,size)

    if typing:
        preview = font_big.render(text+"|", True, color)
        screen.blit(preview,(text_pos[0], text_pos[1]+TOOLBAR_HEIGHT))

    pygame.display.flip()

pygame.quit()