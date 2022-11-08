from math import sqrt
from planet import Planet


# TODO set_price in detail algorithm


class Engine:
    def __init__(self, speed: int):
        self.speed = speed
        self.price = 0


class Tank:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.price = 0
        self.fuel = 0


class Cargo:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 0,
                      'materials': 0,
                      'appliances': 0,
                      'technic': 0,
                      'luxuries': 0
                      }


class StarShip:
    def __init__(self, name: str, cargo: Cargo, location: Planet, engine: Engine = None, tank: Tank = None):
        self.name = name
        self.price = 0
        self.money = 2000
        self.location = location
        self.cargo = cargo
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
            self.cargo = self.ship.cargo

        @property
        def current_capacity(self) -> int:
            return sum([self.cargo.cargo[product] for product in self.cargo.cargo])

        def update_amount(self, product_name: str, amount: int):
            self.cargo.cargo[product_name] += amount

        def __is_valid_product(self, product: str, amount: int) -> bool:
            cargo = self.ship.cargo.cargo
            return isinstance(product, str) and product in cargo and isinstance(amount, int) and amount > 0

        def __is_possible_sale_product(self, product: str, amount: int) -> bool:
            product_amount = self.ship.cargo.cargo[product]
            return amount <= product_amount

        def sale_product(self, product: str, amount: int):
            if self.__is_valid_product(product, amount) and \
                    self.__is_possible_sale_product(product, amount):
                price = self.ship.location.stock.system.get_product(product)[1]
                self.update_amount(product, -amount)
                self.ship.location.stock.system.update_amount(product, amount)
                self.ship.money += price * amount

        def __is_possible_buy_product(self, product: str, amount: int) -> bool:
            product_amount, price = self.ship.location.stock.system.get_product(product)
            difference = self.ship.cargo.capacity - self.ship.system.cargo_module.current_capacity
            return product_amount >= amount and (price * amount <= self.ship.money or
                                                 price * difference <= self.ship.money)

        def buy_product(self, product: str, amount: int):
            if self.__is_valid_product(product, amount) and \
                    self.__is_possible_buy_product(product, amount):
                current_capacity = self.ship.system.cargo_module.current_capacity
                cargo_capacity = self.ship.cargo.capacity
                if amount + current_capacity >= cargo_capacity:
                    amount = cargo_capacity - current_capacity
                self.ship.location.stock.system.update_amount(product, -amount)
                self.ship.money -= self.ship.location.stock.system.get_product(product)[1] * amount
                self.update_amount(product, amount)

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

        @staticmethod
        def __is_valid_fuel(fuel: int) -> bool:
            return isinstance(fuel, int) and fuel > 0

        def __is_possible_refuel(self, fuel: int) -> bool:
            amount, price = self.location.stock.system.get_product('fuel')
            return amount >= fuel and fuel * price <= self.ship.money

        def refuel(self, fuel: int):
            if self.__is_valid_fuel(fuel) and self.__is_possible_refuel(fuel):
                amount, price = self.location.stock.system.get_product('fuel')
                tank_fuel, tank_capacity = self.ship.tank.fuel, self.ship.tank.capacity
                if fuel + tank_fuel >= tank_capacity:
                    fuel = tank_capacity - tank_fuel
                amount -= fuel
                self.location.stock.system.update_amount('fuel', -fuel)
                self.ship.money -= fuel * price
                self.ship.tank.fuel += fuel

        def __is_valid_detail(self, detail: StarShip | Engine | Tank) -> bool:
            return isinstance(detail, StarShip | Engine | Tank) and detail not in \
                   [self.ship, self.ship.tank, self.ship.engine]

        def __is_possible_buy_detail(self, detail: StarShip | Engine | Tank) -> bool:
            return self.location.shop.system.get_price(detail) <= self.ship.money and \
                   detail in self.location.shop.details

        def buy_detail(self, detail: StarShip | Engine | Tank):
            if self.__is_valid_detail(detail) and self.__is_possible_buy_detail(detail):
                price = self.location.shop.system.get_price(detail)
                self.replace_detail(detail)
                self.ship.money -= price

        def sale_detail(self, detail: str):
            if detail == 'Engine':
                self.ship.money += self.ship.engine.price

        def replace_detail(self, detail: StarShip | Engine | Tank):
            detail_type = type(detail).__name__
            if detail_type == 'Engine':
                self.location.shop.details[detail], self.ship.engine = self.ship.engine, detail
            elif detail_type == 'Tank':
                self.location.shop.details[detail], self.ship.tank = self.ship.tank, detail
            else:
                prev_tank, prev_engine = self.ship.tank, self.ship.engine
                self.location.shop.details[detail], self.ship, = self.ship, detail
                self.ship.tank, self.ship.engine = prev_tank, prev_engine


planet1 = Planet('Earth')
planet2 = Planet('Auropa')
star_ship1 = StarShip('qwerty', Cargo(100), planet1, Engine(1), Tank(100))
