from math import sqrt
from planet2 import Planet, Product


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
        self.cargo = [Product(title) for title in
                      ['mineral', 'medicine', 'food', 'material', 'appliance', 'technic', 'luxury']]
        self.engine = engine
        self.tank = tank
        self.system = StarShip.StarShipSystem(self)
        self.control_module = StarShip.ControlModule(self)

    def move_to_planet(self, planet: Planet):
        if planet != self.location:
            distance = self.system.get_distance(planet)
            if self.engine.speed * distance <= self.tank.fuel:
                self.location = planet
                self.tank.fuel -= self.engine.speed * distance

    class StarShipSystem:
        def __init__(self, star_ship):
            self.ship = star_ship
            self.location = self.ship.location

        @property
        def current_capacity(self):
            return sum([product.amount for product in self.ship.cargo])

        def get_distance(self, planet: Planet):
            x, y = (planet.coord[0] - self.location.coord[0]), (planet.coord[1] - self.location.coord[1])
            return round(sqrt(x ** 2 + y ** 2))

        @staticmethod
        def is_valid_fuel(fuel: int) -> bool:
            if isinstance(fuel, int):
                if fuel > 0:
                    return True
            return False

        def is_possible_refuel(self, fuel: int) -> bool:
            if self.location.stock.system.get_product('fuel').amount >= fuel:
                return True
            return False

    class ControlModule:
        def __init__(self, star_ship):
            self.ship = star_ship
            self.location = self.ship.location

        def refuel(self, fuel: int):
            if self.ship.system.is_valid_fuel(fuel) and self.ship.system.is_possible_refuel(fuel):
                if fuel + self.ship.tank.fuel <= self.ship.tank.capacity:
                    self.location.stock.system.get_product('fuel').amount -= fuel
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
planet1.stock.system.update_amount('fuel', 100)
print(star_ship1.tank.fuel)
star_ship1.control_module.refuel(10)
print(star_ship1.tank.fuel)
print(star_ship1.location.name)
star_ship1.move_to_planet(planet2)
print(star_ship1.location.name)
print(star_ship1.tank.fuel)
star_ship1.control_module.refuel(90)
print(star_ship1.tank.fuel)
