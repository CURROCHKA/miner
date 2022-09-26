from star_ship import Engine, Tank, StarShip
from planet import Planet


class Settings:
    def __init__(self):
        self.planets = [Planet('Earth', 'None'), Planet('Auropa', 'None'), Planet('Mars', 'None')]
        self.engines = [Engine(1, 100)]
        self.tanks = [Tank(100, 100)]
        self.star_ships = [StarShip('Buran', 100, self.planets[0], self.engines[0], self.tanks[0])]
