import pygame
import random
import math
from scipy.constants import k  # Import the Boltzmann constant

# Constants
eta = 1e-3  # Viscosity of water in Pa.s
r = 1e-6  # Radius of the water particles in meters


class Medium:
    def __init__(self, width, height, temperature, radius=3):
        self.width = width
        self.height = height
        self.temperature = temperature  # This is the Temperature object
        self.particles = []
        self.particle_radius = radius

        # Number of particles
        self.num_particles = 100
        self.create_particles()

    def create_particles(self):
        # Create particles with random positions and velocities
        for _ in range(self.num_particles):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            # Initial random velocities
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, 1)
            self.particles.append([x, y, vx, vy])

    def calculate_diffusion_coefficient(self):
        # Get the temperature value from the Temperature object
        T = self.temperature.get_temperature()  # Use get_temperature() method

        # Calculate the diffusion coefficient D using Einstein's equation
        D = (k * T) / (6 * math.pi * eta * r)
        return D

    def check_collision(self, p1, p2):
        # Check if two particles collide
        x1, y1, _, _ = p1
        x2, y2, _, _ = p2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < (2 * self.particle_radius)  # Collision if distance is less than 2 * particle radius

    def resolve_collision(self, p1, p2):
        p1[2], p2[2] = p2[2], p1[2]  # Swap vx
        p1[3], p2[3] = p2[3], p1[3]  # Swap vy

    def update(self):
        # Calculate the diffusion coefficient at the current temperature
        D = self.calculate_diffusion_coefficient()

        # Update particle positions based on diffusion
        for i, particle in enumerate(self.particles):
            x, y, vx, vy = particle

            # Diffusion step (random motion)
            # We simulate the random walk by adding a small random step to the position
            step_std = math.sqrt(2 * D)  # Step size proportional to diffusion coefficient

            # Update velocity with random motion
            particle[0] += particle[2] + random.gauss(0, step_std)
            particle[1] += particle[3] + random.gauss(0, step_std)


            # Keep particles within bounds
            if particle[0] - self.particle_radius <= 0 or particle[0] + self.particle_radius >= self.width:
                particle[2] *= -1
            if particle[1] - self.particle_radius <= 0 or particle[1] + self.particle_radius >= self.height:
                particle[3] *= -1

        # Check for collisions between all pairs of particles
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                if self.check_collision(self.particles[i], self.particles[j]):
                    self.resolve_collision(self.particles[i], self.particles[j])

    def draw(self, screen):
        # Draw each particle as a small circle
        for particle in self.particles:
            x, y, _, _ = particle
            pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), self.particle_radius)
