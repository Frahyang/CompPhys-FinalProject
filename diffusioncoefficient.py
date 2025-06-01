import math

# Constants
k_B = 1.380649e-23  # Boltzmann constant in J/K
pi = math.pi

def calculate_diffusion_coefficient(temperature_K, particle_radius_m, eta):
    """
    Stokes-Einstein equation: D = kT / (6 * pi * η * r)
    """
    return k_B * temperature_K / (6 * pi * eta * particle_radius_m)

def calculate_msd(trail):
    """
    Compute mean squared displacement (MSD) from trail points.
    MSD = average of squared distances from starting point.
    """
    if len(trail) < 2:
        return 0

    x0, y0 = trail[0]
    squared_displacements = [(x - x0)**2 + (y - y0)**2 for x, y in trail]
    return sum(squared_displacements) / len(squared_displacements)
