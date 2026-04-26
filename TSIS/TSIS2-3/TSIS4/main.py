import pygame
import sys
from game import SnakeGame, load_settings, save_settings, WIDTH, HEIGHT
from db import create_tables, get_top_10

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)

font = pygame.font.SysFont("Verdana", 24)
big_font = pygame.font.SysFont("Verdana", 48)
small_font = pygame.font.SysFont("Verdana", 18)

settings = load_settings()


def draw_text(text, x, y, color=BLACK, used_font=font):
    img = used_font.render(text, True, color)
    screen.blit(img, (x, y))


def button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)

    label = font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

    return rect


def username_screen():
    username = ""

    while True:
        screen.fill(WHITE)

        draw_text("Enter Username", 210, 160, BLACK, big_font)
        draw_text(username + "|", 300, 270, BLACK, font)
        draw_text("Press ENTER to continue", 260, 350, BLACK, small_font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username.strip():
                    return username.strip()

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode


def main_menu():
    username = username_screen()

    while True:
        screen.fill(WHITE)

        draw_text("Snake Game", 240, 80, GREEN, big_font)
        draw_text(f"Player: {username}", 300, 150, BLACK, small_font)

        play_btn = button("Play", 300, 220, 200, 50)
        leaderboard_btn = button("Leaderboard", 300, 290, 200, 50)
        settings_btn = button("Settings", 300, 360, 200, 50)
        quit_btn = button("Quit", 300, 430, 200, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    game = SnakeGame(screen, username)
                    score, level, best = game.run()
                    game_over_screen(username, score, level, best)

                elif leaderboard_btn.collidepoint(event.pos):
                    leaderboard_screen()

                elif settings_btn.collidepoint(event.pos):
                    settings_screen()

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def game_over_screen(username, score, level, best):
    while True:
        screen.fill(WHITE)

        draw_text("Game Over", 250, 100, RED, big_font)
        draw_text(f"Score: {score}", 320, 210, BLACK)
        draw_text(f"Level: {level}", 320, 250, BLACK)
        draw_text(f"Personal Best Before Game: {best}", 230, 290, BLACK, small_font)

        retry_btn = button("Retry", 300, 370, 200, 50)
        menu_btn = button("Main Menu", 300, 440, 200, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    game = SnakeGame(screen, username)
                    score, level, best = game.run()
                    return game_over_screen(username, score, level, best)

                elif menu_btn.collidepoint(event.pos):
                    return


def leaderboard_screen():
    while True:
        screen.fill(WHITE)

        draw_text("Leaderboard", 250, 50, BLACK, big_font)

        try:
            rows = get_top_10()
        except Exception as e:
            draw_text("Database error", 300, 250, RED)
            rows = []

        y = 130

        draw_text("Rank  Name        Score  Level  Date", 120, 100, BLACK, small_font)

        for i, row in enumerate(rows, start=1):
            username, score, level, played_at = row
            date = str(played_at).split(".")[0]

            text = f"{i}. {username[:10]:10} {score:5} {level:5} {date}"
            draw_text(text, 100, y, BLACK, small_font)
            y += 35

        back_btn = button("Back", 300, 520, 200, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return


def settings_screen():
    global settings

    colors = [
        [0, 200, 0],
        [0, 100, 255],
        [200, 0, 0],
        [240, 220, 0]
    ]

    while True:
        screen.fill(WHITE)

        draw_text("Settings", 290, 80, BLACK, big_font)

        grid_btn = button(f"Grid: {'ON' if settings['grid'] else 'OFF'}", 270, 190, 260, 50)
        sound_btn = button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 270, 260, 260, 50)
        color_btn = button("Change Snake Color", 270, 330, 260, 50)
        save_btn = button("Save & Back", 270, 430, 260, 50)

        pygame.draw.rect(screen, settings["snake_color"], (560, 340, 40, 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(event.pos):
                    current = settings["snake_color"]

                    index = colors.index(current) if current in colors else 0
                    settings["snake_color"] = colors[(index + 1) % len(colors)]

                elif save_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return


if __name__ == "__main__":
    create_tables()
    main_menu()