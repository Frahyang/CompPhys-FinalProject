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
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)

# Initialize clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Initialize simulation objects
temperature = Temperature(600)  # Initial temperature in Kelvin
medium = Medium(WIDTH, HEIGHT, temperature, radius=3)  # Add radius param
liquid = Liquid(WIDTH, HEIGHT, temperature)

def draw_ui():
    temp_text = font.render(f"Temperature: {temperature.get_temperature()} K", True, WHITE)
    radius_text = font.render(f"Particle Radius: {medium.particle_radius}", True, WHITE)
    screen.blit(temp_text, (10, 10))
    screen.blit(radius_text, (10, 35))

def main():
    running = True
    while running:
        screen.fill(GRAY)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle keypresses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    temperature.set_temperature(temperature.get_temperature() + 10)
                elif event.key == pygame.K_DOWN:
                    temperature.set_temperature(max(0, temperature.get_temperature() - 10))
                elif event.key == pygame.K_RIGHT:
                    medium.particle_radius = min(medium.particle_radius + 10, 20)
                elif event.key == pygame.K_LEFT:
                    medium.particle_radius = max(1, medium.particle_radius - 1)

        # Update physics
        medium.update()
        liquid.update(medium.particles, medium.particle_radius)

        # Draw simulation
        medium.draw(screen)
        liquid.draw(screen)
        draw_ui()

        # Refresh screen
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
