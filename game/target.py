import pygame
import random
import math


class Target:
    def __init__(self, game, radius=30, ttl=1.5):
        self.game = game
        self.radius = radius
        self.ttl = ttl  # seconds
        
        self.x = 0
        self.y = 0

        self.time_alive = 0  # how long target has existed

        self.spawn()

    # ------------------------------------------
    # Spawn at random valid position
    # ------------------------------------------
    def spawn(self):
        width = self.game.width
        height = self.game.height

        self.x = random.randint(self.radius, width - self.radius)
        self.y = random.randint(80 + self.radius, height - self.radius)

        self.time_alive = 0

    # ------------------------------------------
    # Update lifetime
    # ------------------------------------------
    def update(self, dt):
        self.time_alive += dt

    # ------------------------------------------
    # Check if expired
    # ------------------------------------------
    def is_expired(self):
        return self.time_alive >= self.ttl

    # ------------------------------------------
    # Check if clicked
    # ------------------------------------------
    def is_hit(self, mouse_pos):
        mx, my = mouse_pos
        distance = math.sqrt((mx - self.x) ** 2 + (my - self.y) ** 2)
        return distance <= self.radius

    # ------------------------------------------
    # Draw target
    # ------------------------------------------
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (129,2,31),  # rgb(129,2,31)
            (self.x, self.y),
            self.radius
        )