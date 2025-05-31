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
            self.particles.append({
                "x": x,
                "y": y,
                "radius": radius,
                "velocity": velocity,
                "trail": []  # ← stores previous positions
            })


    def check_collision(p1, p2, r1, r2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        distance = (dx**2 + dy**2) ** 0.5
        return distance < (r1 + r2)

    def update(self, water_particles, water_radius):
        scale_factor = max(0.1, (self.temperature.get_temperature() / 298))
        for particle in self.particles:
            # Update position
            particle["x"] += particle["velocity"][0] * scale_factor
            particle["y"] += particle["velocity"][1] * scale_factor

            # Wall collision (with radius consideration)
            r = particle["radius"]

            # Left wall
            if particle["x"] - r <= 0:
                particle["x"] = r
                particle["velocity"] = (-particle["velocity"][0], particle["velocity"][1])

            # Right wall
            elif particle["x"] + r >= self.width:
                particle["x"] = self.width - r
                particle["velocity"] = (-particle["velocity"][0], particle["velocity"][1])

            # Top wall
            if particle["y"] - r <= 0:
                particle["y"] = r
                particle["velocity"] = (particle["velocity"][0], -particle["velocity"][1])

            # Bottom wall
            elif particle["y"] + r >= self.height:
                particle["y"] = self.height - r
                particle["velocity"] = (particle["velocity"][0], -particle["velocity"][1])
            
            # Track trajectory
            particle["trail"].append((particle["x"], particle["y"]))

            # Limit trail length to prevent memory buildup
            if len(particle["trail"]) > 10000:
                particle["trail"].pop(0)

            # Collision with water particles
            for water in water_particles:
                wx, wy, wvx, wvy = water
                mx, my = particle["x"], particle["y"]
                mvx, mvy = particle["velocity"]

                dx = mx - wx
                dy = my - wy
                distance = (dx**2 + dy**2)**0.5

                if distance < (r + water_radius + 2):  # Approximate interaction threshold
                    if distance == 0:
                        continue  # Prevent divide-by-zero

                    # Normalized direction vector
                    nx = dx / distance
                    ny = dy / distance

                    # Relative velocity
                    dvx = mvx - wvx
                    dvy = mvy - wvy

                    # Dot product to get velocity component along normal
                    vn = dvx * nx + dvy * ny

                    # Skip if they are moving apart
                    if vn > 0:
                        continue

                    # Apply elastic collision response
                    mvx -= vn * nx
                    mvy -= vn * ny
                    wvx += vn * nx
                    wvy += vn * ny

                    # Update velocities
                    particle["velocity"] = (mvx, mvy)
                    water[2] = wvx
                    water[3] = wvy
                    



    def draw(self, screen):
        for particle in self.particles:
            if len(particle["trail"]) > 1:
                pygame.draw.lines(screen, (255, 255, 150), False, particle["trail"], 2)  # Trail
            pygame.draw.circle(screen, (255, 255, 0), (int(particle["x"]), int(particle["y"])), particle["radius"])  # Particle

    def get_trails(self):
        return [p["trail"] for p in self.particles]