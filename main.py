import pygame
import sys
from medium import Medium
from liquid import Liquid
from temperature import Temperature

# Initialize Pygame
pygame.init()

# Set up screen dimensions and title
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brownian Motion Visualizer")

# Define colors
BLACK = (0, 0, 0)

# Initialize clock
clock = pygame.time.Clock()

# Initialize objects for the simulation
temperature = Temperature(300)  # Set initial temperature (in Kelvin)
medium = Medium(WIDTH, HEIGHT, temperature)
liquid = Liquid(WIDTH, HEIGHT, temperature)

def main():
    running = True
    while running:
        screen.fill(BLACK)  # Clear the screen with white
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the liquid and medium
        medium.update()
        liquid.update(medium.particles)
        
        # Draw the liquid and medium
        medium.draw(screen)
        liquid.draw(screen)

        # Update the display
        pygame.display.flip()
        
        # Set the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
