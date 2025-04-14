import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)  # Random size for particles
        self.color = (0, 0, 0)  # Black color
        self.lifetime = random.randint(20, 50)  # Lifetime of the particle
        self.age = 0
        self.velocity_x = random.uniform(-1, 1)  # Random horizontal velocity
        self.velocity_y = random.uniform(-1, -3)  # Random upward velocity

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.age += 1

    def is_alive(self):
        return self.age < self.lifetime

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size) 