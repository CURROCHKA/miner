from math import sqrt
from product import Product
from planet2 import Planet


class Engine:
    def __init__(self, speed: int):
        self.speed = speed


class Tank:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.fuel = 100


class StarShip:
    def __init__(self, name: str, capacity: int, location: Planet, engine: Engine, tank: Tank):
        self.name = name
        self.location = location
        self.cargo_capacity = capacity
        self.cargo = [Product(title) for title in
                      ['mineral', 'medicine', 'food', 'material', 'appliance', 'technic', 'luxury']]
        self.engine = engine
        self.tank = tank
        self.system = StarShip.StarShipSystem(self)

    def move_to_planet(self, planet):
        if planet != self.location:
            distance = self.system.get_distance(planet)
            if self.engine.speed * distance <= self.tank.fuel:
                self.location = planet
                self.tank.fuel -= self.engine.speed * distance

    class StarShipSystem:
        def __init__(self, star_ship):
            self.ship = star_ship
            self.ship_location = self.ship.location

        @property
        def current_capacity(self):
            return sum([product.amount for product in self.ship.cargo])

        def get_distance(self, planet):
            x, y = (planet.coord[0] - self.ship_location.coord[0]), (planet.coord[1] - self.ship_location.coord[1])
            return round(sqrt(x ** 2 + y ** 2), 1)
