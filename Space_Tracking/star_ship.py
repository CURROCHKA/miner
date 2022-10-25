from math import sqrt
from planet import Planet


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
        self.money = 2000
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

        def get_distance(self, planet: Planet) -> int:
            x, y = (planet.coord[0] - self.location.coord[0]), (planet.coord[1] - self.location.coord[1])
            return round(sqrt(x ** 2 + y ** 2))

    class ControlModule:
        def __init__(self, star_ship: StarShip):
            self.ship = star_ship
            self.location = self.ship.location
            self.cargo = self.ship.cargo
            self.cargo_capacity = self.ship.cargo_capacity
            self.tank = self.ship.tank
            self.stock = self.ship.location.stock
            # self.money = self.ship.money

        @staticmethod
        def is_valid_fuel(fuel: int) -> bool:
            return isinstance(fuel, int) and fuel > 0

        def is_possible_refuel(self, fuel: int) -> bool:
            return self.location.stock.system.get_product('fuel')[0] >= fuel

        def refuel(self, fuel: int):
            if self.is_valid_fuel(fuel) and self.is_possible_refuel(fuel):
                product = self.location.stock.system.get_product('fuel')
                if fuel + self.tank.fuel <= self.tank.capacity:
                    product[0] -= fuel
                    self.ship.money -= fuel * product[1]  # Почему (self.money = self.ship.money) != этой строке?
                    self.tank.fuel += fuel
                else:
                    fuel = self.tank.capacity - self.tank.fuel
                    product[0] -= fuel  # Вот здесь, например, всё работает
                    self.ship.money -= fuel * product[1]
                    self.tank.fuel += fuel

        def is_valid_sale_and_buy(self, product: str, amount: int) -> bool:
            return isinstance(product, str) and product in self.cargo and isinstance(amount, int) and amount > 0

        def sale(self, product: str, amount: int):
            if self.is_valid_sale_and_buy(product, amount):
                self.cargo[product] -= amount
                self.stock.products[product][0] += amount
                self.ship.money += self.location.stock.system.get_product(product)[1] * amount

        def is_possible_buy(self, product: str, amount: int) -> bool:
            return self.location.stock.system.get_product(product)[0] >= amount

        def buy(self, product: str, amount: int):
            if self.is_valid_sale_and_buy(product, amount) and self.is_possible_buy(product, amount):
                if amount + self.ship.system.cargo_module.current_capacity <= self.cargo_capacity:
                    self.location.stock.products[product][0] -= amount
                    self.ship.money -= self.location.stock.system.get_product(product)[1] * amount
                    self.cargo[product] += amount
                else:
                    amount = self.cargo_capacity - self.ship.system.cargo_module.current_capacity
                    self.location.stock.products[product][0] -= amount
                    self.ship.money -= self.location.stock.system.get_product(product)[1] * amount
                    self.cargo[product] += amount


planet1 = Planet('Earth')
planet2 = Planet('Auropa')
star_ship1 = StarShip('qwerty', 100, planet1, Engine(1), Tank(100))
