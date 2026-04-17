import pygame
import sys


class MovingBall:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Moving Ball")

        self.clock = pygame.time.Clock()

        self.radius = 25
        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2

        self.speed = 50

    def move_up(self):
        if self.y - self.speed - self.radius >= 0:
            self.y -= self.speed

    def move_down(self):
        if self.y + self.speed + self.radius <= self.HEIGHT:
            self.y += self.speed

    def move_left(self):
        if self.x - self.speed - self.radius >= 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + self.speed + self.radius <= self.WIDTH:
            self.x += self.speed

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_up()

                    elif event.key == pygame.K_DOWN:
                        self.move_down()

                    elif event.key == pygame.K_LEFT:
                        self.move_left()

                    elif event.key == pygame.K_RIGHT:
                        self.move_right()

            self.screen.fill((255, 255, 255))

            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (self.x, self.y),
                self.radius
            )

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()