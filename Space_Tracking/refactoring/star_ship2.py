from math import sqrt
from refactoring.planet2 import Planet


class Engine:
    def __init__(self, speed: int):
        self.speed = speed
        # self.battery = 0


class Tank:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.fuel = 0


class StarShip:
    def __init__(self, name: str, capacity: int, location: Planet, engine: Engine, tank: Tank):
        self.name = name
        self.location = location
        self.cargo_capacity = capacity
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 0,
                      'materials': 0,
                      'appliances': 0,
                      'technic': 0,
                      'luxuries': 0
                      }
        self.engine = engine
        self.tank = tank
        self.system = ShipSystem(self)

    def move_to_planet(self, planet: Planet):
        if planet != self.location:
            distance = self.system.navigation_module.get_distance(planet)
            if self.engine.speed * distance <= self.tank.fuel:
                self.location = planet
                self.tank.fuel -= self.engine.speed * distance


class ShipSystem:
    def __init__(self, star_ship: StarShip):
        self.ship = star_ship
        self.cargo_module = ShipSystem.CargoModule(self.ship)
        self.navigation_module = ShipSystem.NavigationModule(self.ship)
        self.control_module = ShipSystem.ControlModule(self.ship)

    class CargoModule:
        def __init__(self, star_ship):
            self.ship = star_ship

        @property
        def current_capacity(self) -> int:
            return sum([self.ship.cargo[product] for product in self.ship.cargo])

    class NavigationModule:
        def __init__(self, star_ship: StarShip):
            self.ship = star_ship
            self.location = self.ship.location

        def get_distance(self, planet: Planet):
            x, y = (planet.coord[0] - self.location.coord[0]), (planet.coord[1] - self.location.coord[1])
            return round(sqrt(x ** 2 + y ** 2))

    class ControlModule:
        def __init__(self, star_ship: StarShip):
            self.ship = star_ship
            self.location = self.ship.location

        @staticmethod
        def is_valid_fuel(fuel: int) -> bool:
            if isinstance(fuel, int):
                if fuel > 0:
                    return True
            return False

        def is_possible_refuel(self, fuel: int) -> bool:
            if self.location.stock.system.get_product('fuel')[0] >= fuel:
                return True
            return False

        def refuel(self, fuel: int):
            if self.is_valid_fuel(fuel) and self.is_possible_refuel(fuel):
                if fuel + self.ship.tank.fuel <= self.ship.tank.capacity:
                    self.location.stock.system.get_product('fuel')[0] -= fuel
                    self.ship.tank.fuel += fuel
                else:
                    self.ship.tank.fuel += self.ship.tank.capacity - self.ship.tank.fuel

        def sale(self, product: str, amount: int):
            pass

        def buy(self, product: str, amount: int):
            pass


planet1 = Planet('Earth')
planet2 = Planet('Auropa')
star_ship1 = StarShip('qwerty', 100, planet1, Engine(1), Tank(100))
star_ship1.system.control_module.refuel(100)
print(star_ship1.location.name)
star_ship1.move_to_planet(planet2)
print(star_ship1.location.name)
