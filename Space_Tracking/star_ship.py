from typing import Union
from planet import Planet, Stock, Shop
from math import sqrt


class Engine:
    def __init__(self, speed: int, price: int):
        self.speed = speed
        self.price = price


class Tank:
    def __init__(self, capacity: int, price: int):
        self.capacity = capacity
        self.price = price
        self.fuel = 0


class CargoBay:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 0,
                      'materials': 0,
                      'appliances': 0,
                      'machinery': 0,
                      'luxuries': 0
                      }


class StarShip:
    def __init__(self, name: str, capacity: int, location: Planet, engine: Engine = None, tank: Tank = None):
        self.name = name
        self.money = 2000
        self.location = location
        self.cargo_bay = CargoBay(capacity)
        self.engine = engine
        self.tank = tank
        self.ship_system = ShipSystem()

    def is_enough_money(self, cost: int):
        if cost <= self.money:
            return True
        print(f"Not enough money for the buy. You need additional {cost - self.money}$.")
        return False

    @staticmethod
    def get_component_name(component: Union[Engine, Tank]) -> str:
        return component.__class__.__name__.lower()

    def make_sale(self, product: str, amount: int):
        result = self.ship_system.CargoModule.sale_product(product, amount, self.cargo_bay, self.location.stock)
        if result:
            stock = self.location.stock
            income = stock.products[product][1] * amount
            self.money += income
            print(
                f"Sale of {amount} {product} units for {income}$ is complete. Current balance is {self.money}$.")
        else:
            print(f"Sale is denied. There is no possibility to sale {amount} units of {product}.")

    def make_buy(self, product: str, amount: int):
        stock = self.location.stock
        cost = stock.products[product][1] * amount
        if (self.is_enough_money(cost) and
                self.ship_system.CargoModule.buy_product(product, amount, self.cargo_bay, stock)):
            self.money -= cost
            print(
                f"Buying of {amount} {product} units for {cost}$ is complete. Current balance is {self.money}$.")
        else:
            print(f"Buying is denied. There is no possibility to buy {amount} units of {product}.")

    def move_to_planet(self, target_planet: Planet):
        planet_name = target_planet.name
        result = self.ship_system.NavigationModule.move_to_planet(target_planet, self)
        if result:
            print(f"You have arrived on the planet {planet_name}.")
        else:
            print(f"There is no possibility to move to a planet {planet_name}.")

    def make_refuel(self, refuel_amount: int):
        stock = self.location.stock
        cost = stock.products["fuel"][1] * refuel_amount
        if self.is_enough_money(cost) and self.ship_system.ComponentModule.refuel(refuel_amount, self.tank, stock):
            self.money -= cost
            print(
                f"Refuel of {refuel_amount} units for {cost}$ is complete. Current balance is {self.money}$.")
        else:
            print(f"Refuel is denied. There is no possibility to refuel {refuel_amount} units of fuel.")

    def buy_new_component(self, component: Union[Engine, Tank]):
        shop = self.location.shop
        cost = component.price
        cost_old_component = self.engine.price if isinstance(component, Engine) else self.tank.price
        component_name = self.get_component_name(component)
        if (self.is_enough_money(cost - cost_old_component) and
                self.ship_system.ComponentModule.buy_component(component, shop, self)):
            self.sale_old_component(component_name, cost_old_component)
            self.money -= cost
            print(f"Bought a new component - {component_name} for {cost}$. Current balance is {self.money}$.")
        else:
            print(f"Purchase is denied. There is no possibility to buy {component_name}.")

    def sale_old_component(self, component_name: str, cost: int):
        self.money += cost
        print(f"Your {component_name} was sold for {cost}$.")

    def get_information(self):
        pass


class ShipSystem:
    class CargoModule:
        @staticmethod
        def get_current_capacity(cargo: dict) -> int:
            return sum(cargo.values())

        @staticmethod
        def sale_product(product: str, sale_amount: int, cargo_bay: CargoBay, stock: Stock) -> bool:
            cargo_bay_product_amount = cargo_bay.cargo[product]
            if not (product in cargo_bay.cargo and sale_amount <= cargo_bay_product_amount):
                return False
            cargo_bay.cargo[product] -= sale_amount
            stock.products[product][0] += sale_amount
            return True

        @staticmethod
        def buy_product(product: str, buy_amount: int, cargo_bay: CargoBay, stock: Stock) -> bool:
            cargo_bay_current_capacity = ShipSystem.CargoModule.get_current_capacity(cargo_bay.cargo)
            stock_amount = stock.products[product][0]
            if not (product in cargo_bay.cargo
                    and buy_amount <= cargo_bay.capacity - cargo_bay_current_capacity
                    and buy_amount <= stock_amount):
                return False
            cargo_bay.cargo[product] += buy_amount
            stock.products[product][0] -= buy_amount
            return True

    class NavigationModule:
        @staticmethod
        def get_distance(current_planet: Planet, target_planet: Planet) -> int:
            x = target_planet.coord[0] - current_planet.coord[0]
            y = target_planet.coord[1] - current_planet.coord[1]
            return round(sqrt(x ** 2 + y ** 2))

        @staticmethod
        def move_to_planet(target_planet: Planet, ship: StarShip) -> bool:
            distance = ship.ship_system.NavigationModule.get_distance(ship.location, target_planet)
            speed = ship.engine.speed
            fuel = ship.tank.fuel
            location = ship.location
            if speed * distance <= fuel and not(target_planet is location):
                ship.location = target_planet
                ship.tank.fuel -= speed * distance
                return True
            return False

    class ComponentModule:
        @staticmethod
        def refuel(refuel_amount: int, tank: Tank, stock: Stock) -> bool:
            stock_amount = stock.products["fuel"][0]
            if not (refuel_amount <= stock_amount and refuel_amount + tank.fuel <= tank.capacity):
                return False
            tank.fuel += refuel_amount
            stock.products["fuel"][0] -= refuel_amount
            return True

        @staticmethod
        def buy_component(component: Union[Engine, Tank], shop: Shop, ship: StarShip) -> bool:
            if not (component in shop.components):
                return False
            if isinstance(component, Engine):
                ship.engine = component
            elif isinstance(component, Tank):
                ship.ship_system.ComponentModule.sale_component(component, shop, ship)
                fuel = ship.tank.fuel if ship.tank.fuel <= component.capacity else component.capacity
                ship.tank = component
                ship.tank.fuel = fuel
            shop.components.remove(component)
            return True

        @staticmethod
        def sale_component(component: Union[Engine, Tank], shop: Shop, ship: StarShip):
            if isinstance(component, Engine):
                shop.components.append(ship.engine)
            elif isinstance(component, Tank):
                shop.components.append(ship.tank)

    class InformationModule:
        @staticmethod
        def get_planet_info(planet):
            pass

        @staticmethod
        def get_stock_info(planet):
            pass


planet1 = Planet('Earth')
planet2 = Planet('Auropa')
star_ship1 = StarShip('qwerty', 1000, planet1, Engine(1, 20), Tank(100, 50))
