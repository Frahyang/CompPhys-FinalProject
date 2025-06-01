import pygame as pg
import sys
from medium import Medium
from liquid import Liquid
from temperature import Temperature
from diffusioncoefficient import calculate_diffusion_coefficient, calculate_msd
from viscosity import Viscosity
import time

# Initialize pygame
pg.init()

# Set up screen dimensions and title
SIM_WIDTH, HEIGHT = 800, 600
CONTROLLER_WIDTH = 200
TOTAL_WIDTH = SIM_WIDTH + CONTROLLER_WIDTH
screen = pg.display.set_mode((TOTAL_WIDTH, HEIGHT))
pg.display.set_caption("Brownian Motion Visualizer")

# Define colors
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)

# Initialize clock and font
clock = pg.time.Clock()
font = pg.font.SysFont(None, 24)

# Initialize simulation objects
current_viscosity = Viscosity()
temperature = Temperature(298)  # Initial temperature in Kelvin
medium = Medium(SIM_WIDTH, HEIGHT, temperature, current_viscosity, radius=20)  # Add radius param
liquid = Liquid(SIM_WIDTH, HEIGHT, temperature)

stopped = False

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = (100, 100, 100)

    def draw(self, surface, font):
        pg.draw.rect(surface, self.color, self.rect)
        label = font.render(self.text, True, (255, 255, 255))
        surface.blit(label, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pg.Rect(x, y, width, height)
        self.handle_rect = pg.Rect(0, 0, 10, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.update_handle_position()

    def update_handle_position(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.x = self.rect.x + int(ratio * (self.rect.width - self.handle_rect.width))
        self.handle_rect.y = self.rect.y

    def draw(self, surface, font):
        # Slider line
        pg.draw.rect(surface, (200, 200, 200), self.rect)
        # Handle
        pg.draw.rect(surface, (0, 0, 255), self.handle_rect)
        # Label and value
        label_surface = font.render(f"{self.label}: {int(self.value)}", True, WHITE)
        surface.blit(label_surface, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            new_x = min(max(mouse_x, self.rect.x), self.rect.x + self.rect.width - self.handle_rect.width)
            self.handle_rect.x = new_x

            # Update value based on handle position
            ratio = (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

def reset_simulation():
    global start_time
    for p in liquid.particles:
        p["trail"].clear()
    start_time = time.time()

def stop_simulation():
    global stopped

    stopped = True
    elapsed_time = time.time() - start_time

    D = calculate_diffusion_coefficient(
        temperature.get_temperature(),
        50e-6,
        current_viscosity.get_viscosity(temperature.get_temperature())
    )

    msd = calculate_msd(liquid.particles[0]["trail"]) * 1e-17  # Scale factor
    expected_msd = 4 * D * elapsed_time

    print(f"\n=== Simulation Results ===")
    print(f"Diffusion Coefficient: {D:.3e} m²/s")
    print(f"Mean Squared Displacement: {msd:.3e} m²")
    print(f"Expected MSD: {expected_msd:.3e} m²")
    print(f"Time: {elapsed_time:.1f} s\n")

buttons = [
    Button(SIM_WIDTH + 30, 340, 140, 30, "Reset", reset_simulation),
    Button(SIM_WIDTH + 30, 380, 140, 30, "Record", stop_simulation),
]

def draw_ui():
    # Draw control panel background
    pg.draw.rect(screen, (50, 50, 50), (SIM_WIDTH, 0, CONTROLLER_WIDTH, HEIGHT))  # Dark gray panel
    # Draw vertical separator
    pg.draw.line(screen, WHITE, (SIM_WIDTH, 0), (SIM_WIDTH, HEIGHT), 2)
    # Draw sliders
    temp_slider.draw(screen, font)
    radius_slider.draw(screen, font)
    for button in buttons:
        button.draw(screen, font)



temp_slider = Slider(SIM_WIDTH + 30, 100, 140, 20, 273, 373, temperature.get_temperature(), "Temperature (K)")
radius_slider = Slider(SIM_WIDTH + 30, 160, 140, 20, 1, 20, medium.particle_radius, "Radius")


start_time = time.time()
def main():
    running = True
    while running:
        screen.fill(GRAY)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            temp_slider.handle_event(event)
            radius_slider.handle_event(event)
            for button in buttons:
                button.handle_event(event)
        
        # Sync slider values to simulation
        temperature.set_temperature(temp_slider.value)
        medium.particle_radius = int(radius_slider.value)

        # Update physics
        medium.update()
        liquid.update(medium.particles, medium.particle_radius)

        # Draw simulation
        medium.draw(screen)
        liquid.draw(screen)
        draw_ui()

        elapsed_time = time.time() - start_time
        stopwatch_text = font.render(f"Time: {elapsed_time:.1f}s", True, WHITE)
        screen.blit(stopwatch_text, (SIM_WIDTH + 30, 220))

        # Refresh screen
        pg.display.flip()
        clock.tick(60)
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
