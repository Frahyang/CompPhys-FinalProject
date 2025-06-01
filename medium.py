import pygame
import random
import math
from scipy.constants import k  # Import the Boltzmann constant

class Medium:
    def __init__(self, width, height, temperature, current_viscosity, radius):
        self.width = width
        self.height = height
        self.temperature = temperature  # This is the Temperature object
        self.current_viscosity = current_viscosity
        self.particles = []
        self.particle_radius = radius

        # Number of particles
        self.num_particles = 200
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
        eta = self.current_viscosity.get_viscosity(T)
        r_meters = self.particle_radius * 1e-6
        # Calculate the diffusion coefficient D using Einstein's equation
        D = (k * T) / (6 * math.pi * eta * r_meters)
        return D

    def check_collision(self, p1, p2):
        # Check if two particles collide
        x1, y1, _, _ = p1
        x2, y2, _, _ = p2
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance < (2 * self.particle_radius)  # Collision if distance is less than 2 * particle radius

    def resolve_collision(self, p1, p2):
        x1, y1, vx1, vy1 = p1
        x2, y2, vx2, vy2 = p2

        dx = x1 - x2
        dy = y1 - y2
        distance = math.hypot(dx, dy)

        if distance == 0:
            return  # Avoid division by zero

        # Normalized collision vector, dot product
        nx = dx / distance
        ny = dy / distance

        # Relative velocity
        dvx = vx1 - vx2
        dvy = vy1 - vy2

        # Velocity component along the normal
        vn = dvx * nx + dvy * ny

        # Skip if particles are moving away from each other
        if vn > 0:
            return

        # Compute new velocities (elastic collision for equal mass)
        p1[2] -= vn * nx
        p1[3] -= vn * ny
        p2[2] += vn * nx
        p2[3] += vn * ny

    def update(self):
        # Calculate the diffusion coefficient at the current temperature
        D = self.calculate_diffusion_coefficient()

        T = self.temperature.get_temperature()

        scale_factor = (T - 273) / 10

        # Update particle positions based on diffusion
        for i, particle in enumerate(self.particles):

            # Diffusion step (random motion)
            step_std = math.sqrt(2 * D)  # Step size proportional to diffusion coefficient

            # Update velocity with random motion
            particle[0] += (particle[2] * scale_factor) + random.gauss(0, step_std)
            particle[1] += (particle[3] * scale_factor) + random.gauss(0, step_std)

            # Keep particles within bounds and reposition if needed
            if particle[0] - self.particle_radius <= 0:
                particle[0] = self.particle_radius  # push inside
                particle[2] *= -1                   # reflect x velocity
            elif particle[0] + self.particle_radius >= self.width:
                particle[0] = self.width - self.particle_radius
                particle[2] *= -1

            if particle[1] - self.particle_radius <= 0:
                particle[1] = self.particle_radius
                particle[3] *= -1                   # reflect y velocity
            elif particle[1] + self.particle_radius >= self.height:
                particle[1] = self.height - self.particle_radius
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
