import pygame
import os
import sys


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.WIDTH = 800
        self.HEIGHT = 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Music Player")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.playlist = [
            os.path.join("songs", "track1.wav"),
            os.path.join("songs", "track2.wav")
        ]

        self.current_track_index = 0
        self.is_playing = False
        self.status = "Stopped"

    def load_track(self):
        track_path = self.playlist[self.current_track_index]
        pygame.mixer.music.load(track_path)

    def play_track(self):
        self.load_track()
        pygame.mixer.music.play()
        self.is_playing = True
        self.status = "Playing"

    def stop_track(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.status = "Stopped"

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_track()

    def previous_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play_track()

    def get_current_track_length(self):
        track_path = self.playlist[self.current_track_index]
        sound = pygame.mixer.Sound(track_path)
        return sound.get_length()

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02}:{secs:02}"

    def draw_progress_bar(self, current_time, total_time):
        bar_x = 150
        bar_y = 260
        bar_width = 500
        bar_height = 20

        pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))

        if total_time > 0:
            progress_width = (current_time / total_time) * bar_width
            progress_width = min(progress_width, bar_width)
            pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, progress_width, bar_height))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play_track()

                    elif event.key == pygame.K_s:
                        self.stop_track()

                    elif event.key == pygame.K_n:
                        self.next_track()

                    elif event.key == pygame.K_b:
                        self.previous_track()

                    elif event.key == pygame.K_q:
                        running = False

            self.screen.fill((30, 30, 30))

            title_text = self.font.render("Music Player", True, (255, 255, 255))
            self.screen.blit(title_text, (280, 40))

            current_name = os.path.basename(self.playlist[self.current_track_index])
            track_text = self.small_font.render(f"Current track: {current_name}", True, (255, 255, 255))
            self.screen.blit(track_text, (220, 110))

            status_text = self.small_font.render(f"Status: {self.status}", True, (255, 255, 255))
            self.screen.blit(status_text, (320, 150))

            current_seconds = 0
            total_seconds = self.get_current_track_length()

            if self.is_playing:
                pos_ms = pygame.mixer.music.get_pos()
                if pos_ms >= 0:
                    current_seconds = pos_ms / 1000

            time_text = self.small_font.render(
                f"Position: {self.format_time(current_seconds)} / {self.format_time(total_seconds)}",
                True,
                (255, 255, 255)
            )
            self.screen.blit(time_text, (220, 210))

            self.draw_progress_bar(current_seconds, total_seconds)

            controls_text = self.small_font.render(
                "P = Play   S = Stop   N = Next   B = Back   Q = Quit",
                True,
                (200, 200, 200)
            )
            self.screen.blit(controls_text, (100, 330))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()