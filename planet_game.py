import pygame
import os
from planet_platformer import PlanetPlatformer, Player
from space5 import planets

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Planet Explorer")
    
    # Example of creating a platformer for each planet
    planet_name = "Mars"  # Change this to test different planets
    
    # Create the platformer game for the selected planet
    game = PlanetPlatformer(
        planet_name=planet_name,
        planet_color=planets[planet_name]["color"],
        planet_info=planets[planet_name]["info"],
        background_color=(0, 0, 0)  # Black background for space
    )
    
    # Run the game
    game.run()
    
    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main() 