import pygame
import datetime
from tools import flood_fill

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 1000, 800 # Увеличили высоту для панели
TOOLBAR_HEIGHT = 100
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint Pro")

# Основной холст (отдельная поверхность)
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# Состояние
active_color = BLACK
active_size = 2
tool = "pencil" # pencil, line, rect, circle, square, triangle, fill, text
drawing = False
typing = False
text_content = ""
text_pos = (0, 0)
font_small = pygame.font.SysFont("Arial", 18)
font_main = pygame.font.SysFont("Arial", 24)

def draw_ui():
    """Отрисовка верхней панели инструментов"""
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)
    
    # Список инструментов для отображения
    tools_list = ["pencil", "line", "rect", "circle", "square", "triangle", "fill", "text"]
    for i, t in enumerate(tools_list):
        rect = pygame.Rect(10 + i * 85, 10, 80, 35)
        color = (180, 180, 180) if tool == t else (210, 210, 210)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        txt = font_small.render(t.capitalize(), True, BLACK)
        screen.blit(txt, (rect.x + 5, rect.y + 8))

    # Выбор размера (1, 2, 3)
    sizes = [2, 5, 10]
    for i, s in enumerate(sizes):
        rect = pygame.Rect(10 + i * 40, 55, 35, 35)
        color = (180, 180, 180) if active_size == s else (210, 210, 210)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)
        pygame.draw.circle(screen, BLACK, rect.center, s if s < 15 else 15)

    # Индикаторы текущего состояния
    status_txt = font_small.render(f"Tool: {tool} | Size: {active_size}px | Ctrl+S to Save", True, BLACK)
    screen.blit(status_txt, (700, 70))
    
    # Текущий цвет
    pygame.draw.rect(screen, active_color, (900, 15, 70, 40))
    pygame.draw.rect(screen, BLACK, (900, 15, 70, 40), 2)

def draw_shape(surf, tool_type, color, start, end, size):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    
    if tool_type == "line":
        pygame.draw.line(surf, color, start, end, size)
    elif tool_type == "rect":
        pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), size)
    elif tool_type == "circle":
        radius = int(((dx**2) + (dy**2))**0.5)
        pygame.draw.circle(surf, color, start, radius, size)
    elif tool_type == "square":
        side = max(abs(dx), abs(dy))
        pygame.draw.rect(surf, color, (x1, y1, side, side), size)
    elif tool_type == "triangle":
        pygame.draw.polygon(surf, color, [start, (x1, y2), end], size)

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    draw_ui()
    
    mouse_pos = pygame.mouse.get_pos()
    # Координаты мыши относительно холста
    adj_mouse_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Клик по панели инструментов
            if mouse_pos[1] < TOOLBAR_HEIGHT:
                # Проверка выбора инструмента
                for i in range(8):
                    if 10 + i * 85 <= mouse_pos[0] <= 90 + i * 85 and 10 <= mouse_pos[1] <= 45:
                        tool = ["pencil", "line", "rect", "circle", "square", "triangle", "fill", "text"][i]
                # Проверка выбора размера
                for i, s in enumerate([2, 5, 10]):
                    if 10 + i * 40 <= mouse_pos[0] <= 45 + i * 40 and 55 <= mouse_pos[1] <= 90:
                        active_size = s
            
            # Клик по холсту
            else:
                if tool == "fill":
                    flood_fill(canvas, adj_mouse_pos[0], adj_mouse_pos[1], active_color)
                elif tool == "text":
                    typing = True
                    text_pos = adj_mouse_pos
                    text_content = ""
                else:
                    drawing = True
                    start_pos = adj_mouse_pos
                    last_pos = adj_mouse_pos

        if event.type == pygame.MOUSEMOTION and drawing:
            if tool == "pencil":
                pygame.draw.line(canvas, active_color, last_pos, adj_mouse_pos, active_size)
                last_pos = adj_mouse_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool != "pencil":
                draw_shape(canvas, tool, active_color, start_pos, adj_mouse_pos, active_size)
            drawing = False

        # Обработка текста и горячих клавиш
        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    txt_surf = font_main.render(text_content, True, active_color)
                    canvas.blit(txt_surf, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                fn = f"paint_{datetime.datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(canvas, fn)

    # Предпросмотр (Live Preview)
    if drawing and tool != "pencil":
        # Рисуем на screen, смещая координаты на TOOLBAR_HEIGHT
        preview_start = (start_pos[0], start_pos[1] + TOOLBAR_HEIGHT)
        draw_shape(screen, tool, active_color, preview_start, mouse_pos, active_size)
    
    if typing:
        preview_txt = font_main.render(text_content + "|", True, active_color)
        screen.blit(preview_txt, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    pygame.display.flip()

pygame.quit()