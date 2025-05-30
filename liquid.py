import pygame
import random

class Liquid:
    def __init__(self, width, height, temperature):
        self.width = width
        self.height = height
        self.temperature = temperature
        self.particles = []

        # Number of milk particles
        self.num_particles = 1
        self.create_particles()

    def create_particles(self):
        # Create milk particles (slightly larger circles)
        for _ in range(self.num_particles):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            radius = 8
            velocity = random.uniform(-1, 1), random.uniform(-1, 1)
            self.particles.append({"x": x, "y": y, "radius": radius, "velocity": velocity})

    def check_collision(p1, p2, r1, r2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        distance = (dx**2 + dy**2) ** 0.5
        return distance < (r1 + r2)

    def update(self, water_particles, water_radius):
        for particle in self.particles:
            # Update position
            particle["x"] += particle["velocity"][0]
            particle["y"] += particle["velocity"][1]

            # Wall collision (with radius consideration)
            r = particle["radius"]
            if particle["x"] - r <= 0 or particle["x"] + r >= self.width:
                particle["velocity"] = (-particle["velocity"][0], particle["velocity"][1])
            if particle["y"] - r <= 0 or particle["y"] + r >= self.height:
                particle["velocity"] = (particle["velocity"][0], -particle["velocity"][1])

            # Collision with water particles
            for water in water_particles:
                dx = water[0] - particle["x"]
                dy = water[1] - particle["y"]
                distance = (dx**2 + dy**2)**0.5
                if distance < (r + water_radius):  # 3 = water radius
                    # Swap velocities
                    water[2], particle["velocity"] = particle["velocity"][0], (water[2], particle["velocity"][1])
                    water[3], particle["velocity"] = particle["velocity"][1], (particle["velocity"][0], water[3])
                    # Flatten the velocity tuple
                    particle["velocity"] = (particle["velocity"][0], particle["velocity"][1])
                


    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, (255, 255, 0), (int(particle["x"]), int(particle["y"])), particle["radius"])
