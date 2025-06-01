import math

class Viscosity:
    def __init__(self):
        self.liquid = "water"

    def get_viscosity(self, temperature_K):
        return self.water_viscosity(temperature_K)

    def water_viscosity(self, T_K):
        T_C = T_K - 273.15
        return 2.414e-5 * 10**(247.8 / (T_C + 133.15))  # in Pa·s
    