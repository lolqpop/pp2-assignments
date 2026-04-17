import pygame
import sys
import os
from datetime import datetime


class MickeyClock:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mickey Clock")

        self.clock = pygame.time.Clock()

        self.center_x = self.WIDTH // 2
        self.center_y = self.HEIGHT // 2

        clock_path = os.path.join("images", "clock.png")
        self.clock_image = pygame.image.load(clock_path).convert_alpha()
        self.clock_image = pygame.transform.scale(self.clock_image, (700, 700))
        self.image_rect = self.clock_image.get_rect(center=(self.center_x, self.center_y))

        right_hand_path = os.path.join("images", "right.png")
        left_hand_path = os.path.join("images", "left.png")

        self.right_hand = pygame.image.load(right_hand_path).convert_alpha()
        self.left_hand = pygame.image.load(left_hand_path).convert_alpha()

        self.right_hand = pygame.transform.scale(self.right_hand, (180, 60))
        self.left_hand = pygame.transform.scale(self.left_hand, (220, 60))

    def run(self):
        running = True

        while running:
            
            current_time = datetime.now()
           
            minutes = current_time.minute
            seconds = current_time.second

            milliseconds = current_time.microsecond / 1_000_000

            second_angle = -((seconds + milliseconds) * 6)
            minute_angle = -((minutes + (seconds + milliseconds) / 60) * 6)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.clock_image, self.image_rect)

            start_angle = 90  
            
            for hand, angle in [(self.right_hand, minute_angle), (self.left_hand, second_angle)]:
             
                final_angle = start_angle + angle
                
                rotated_hand = pygame.transform.rotate(hand, final_angle)
                
          
                offset = pygame.math.Vector2(hand.get_width() // 2, 0) 
                offset.rotate_ip(-final_angle)
                
                rect = rotated_hand.get_rect(center=(self.center_x + offset.x, self.center_y + offset.y))
                self.screen.blit(rotated_hand, rect)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()