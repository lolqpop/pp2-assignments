import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)

_font_cache = {}


def font(size=20):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.SysFont("Verdana", size)
    return _font_cache[size]


def draw_text(screen, text, x, y, color=BLACK, size=20):
    img = font(size).render(text, True, color)
    screen.blit(img, (x, y))


def button(screen, text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    label = font(20).render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

    return rect