import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
RED = (220, 40, 40)


def font(size=20):
    return pygame.font.SysFont("Verdana", size)


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