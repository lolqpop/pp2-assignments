import pygame
import sys
from ui import button, draw_text
from racer import play_game
from persistence import load_settings, save_settings, load_leaderboard

pygame.init()
pygame.mixer.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Racer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)

settings = load_settings()


def username_screen():
    name = ""

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Enter Username", 60, 150, BLACK, 34)
        draw_text(screen, name + "|", 100, 250, BLACK, 30)
        draw_text(screen, "Press ENTER to start", 85, 340, BLACK, 18)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode


def leaderboard_screen():
    while True:
        screen.fill(WHITE)

        draw_text(screen, "Leaderboard", 70, 40, BLACK, 34)

        data = load_leaderboard()

        y = 100
        if not data:
            draw_text(screen, "No scores yet", 120, 250, BLACK, 20)
        else:
            for i, item in enumerate(data[:10], start=1):
                text = f"{i}. {item['name']} | {item['score']} | {item['distance']}m"
                draw_text(screen, text, 25, y, BLACK, 15)
                y += 35

        back_btn = button(screen, "Back", 100, 520, 200, 45)

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

    colors = ["blue", "red", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Settings", 100, 60, BLACK, 34)

        sound_btn = button(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", 80, 150, 240, 45)
        color_btn = button(screen, f"Car: {settings['car_color']}", 80, 220, 240, 45)
        diff_btn = button(screen, f"Difficulty: {settings['difficulty']}", 80, 290, 240, 45)
        back_btn = button(screen, "Back", 80, 420, 240, 45)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif color_btn.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]
                    save_settings(settings)

                elif diff_btn.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                    save_settings(settings)

                elif back_btn.collidepoint(event.pos):
                    return


def game_over_screen(username, score, distance, coins):
    while True:
        screen.fill(WHITE)

        draw_text(screen, "Game Over", 75, 90, RED, 38)
        draw_text(screen, f"Score: {score}", 120, 190, BLACK, 20)
        draw_text(screen, f"Distance: {distance}m", 120, 225, BLACK, 20)
        draw_text(screen, f"Coins: {coins}", 120, 260, BLACK, 20)

        retry_btn = button(screen, "Retry", 90, 350, 220, 45)
        menu_btn = button(screen, "Main Menu", 90, 420, 220, 45)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    result, score, distance, coins = play_game(screen, username, settings)

                    if result == "game_over":
                        return game_over_screen(username, score, distance, coins)

                    return

                elif menu_btn.collidepoint(event.pos):
                    return


def main_menu():
    while True:
        screen.fill(WHITE)

        draw_text(screen, "Racer Game", 65, 80, BLACK, 36)

        play_btn = button(screen, "Play", 100, 190, 200, 45)
        leaderboard_btn = button(screen, "Leaderboard", 100, 255, 200, 45)
        settings_btn = button(screen, "Settings", 100, 320, 200, 45)
        quit_btn = button(screen, "Quit", 100, 385, 200, 45)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    username = username_screen()
                    result, score, distance, coins = play_game(screen, username, settings)

                    if result == "game_over":
                        game_over_screen(username, score, distance, coins)

                elif leaderboard_btn.collidepoint(event.pos):
                    leaderboard_screen()

                elif settings_btn.collidepoint(event.pos):
                    settings_screen()

                elif quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


main_menu()