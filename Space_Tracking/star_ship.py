from typing import Union
from planet import Planet, Stock, Shop
from math import sqrt


class Engine:
    def __init__(self, speed: int, price: int):
        self.speed = speed
        self.price = price


class Tank:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.price = 0
        self.fuel = 0


class CargoBay:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 100,
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
        print(f"Not enough money for the buy. You need additional {cost - self.money}$")
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
                f"Sale of {amount} {product} units for {income}$ is complete. Current balance is {self.money}")
        else:
            print(f"Sale is denied. There is no possibility to sale {amount} units of {product}")

    def make_buy(self, product: str, amount: int):
        stock = self.location.stock
        cost = stock.products[product][1] * amount
        result = self.ship_system.CargoModule.buy_product(product, amount, self.cargo_bay, stock)
        if self.is_enough_money(cost) and result:
            self.money -= cost
            print(
                f"Buying of {amount} {product} units for {cost}$ is complete. Current balance is {self.money}")
        else:
            print(f"Buying is denied. There is no possibility to buy {amount} units of {product}")

    def move_to_planet(self, target_planet: Planet):
        if target_planet is self.location:
            distance = self.ship_system.NavigationModule.get_distance(self.location, target_planet)
            if self.engine.speed * distance <= self.tank.fuel:
                self.location = target_planet
                self.tank.fuel -= self.engine.speed * distance

    def make_refuel(self, refuel_amount: int):
        stock = self.location.stock
        cost = stock.products["fuel"][1] * refuel_amount
        result = self.ship_system.ComponentModule.refuel(refuel_amount, self.tank, stock)
        if self.is_enough_money(cost) and result:
            self.money -= cost
            print(
                f"Refuel of {refuel_amount} units for {cost}$ is complete. Current balance is {self.money}")
        else:
            print(f"Refuel is denied. There is no possibility to refuel {refuel_amount} units of fuel")

    def buy_new_component(self, component: Union[Engine, Tank]):
        shop = self.location.shop
        cost = component.price
        cost -= self.engine.price if isinstance(component, Engine) else self.tank.price
        result = self.ship_system.ComponentModule.buy_component(component, shop, self)
        component_name = self.get_component_name(component)
        if self.is_enough_money(cost) and result:
            # self.sale_old_component(component)
            self.money -= cost
            cost = cost if cost >= 0 else 0
            print(f"Bought a new detail - {component_name} for a {cost}$. Current balance is {self.money}")
        else:
            print(f"Purchase is denied. There is no possibility to buy {component_name}")

    def sale_old_component(self, component: Union[Engine, Tank]):
        shop = self.location.shop
        income = 0
        if isinstance(component, Engine):
            income = self.engine.price
            shop.details.append(self.engine)
        elif isinstance(component, Tank):
            income = self.tank.price
            shop.details.append(self.tank)
        component_name = self.get_component_name(component)
        print(f"Your {component_name} was sold for {income}$")

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
            if not (product in cargo_bay.cargo and 0 < sale_amount <= cargo_bay_product_amount):
                return False
            cargo_bay.cargo[product] -= sale_amount
            stock.products[product][0] += sale_amount
            return True

        @staticmethod
        def buy_product(product: str, buy_amount: int, cargo_bay: CargoBay, stock: Stock) -> bool:
            cargo_bay_current_capacity = ShipSystem.CargoModule.get_current_capacity(cargo_bay.cargo)
            stock_amount = stock.products[product][0]
            if not (product in cargo_bay.cargo.keys()
                    and 0 < buy_amount <= cargo_bay_current_capacity
                    and buy_amount <= stock_amount
            ):
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

    class ComponentModule:
        @staticmethod
        def refuel(refuel_amount: int, tank: Tank, stock: Stock) -> bool:
            refuel_amount = refuel_amount if refuel_amount <= tank.capacity - tank.fuel else tank.capacity - tank.fuel
            stock_amount = stock.products["fuel"][1]
            if not refuel_amount <= stock_amount:
                return False
            tank.fuel += refuel_amount
            stock.products["fuel"][0] -= refuel_amount
            return True

        @staticmethod
        def buy_component(component: Union[Engine, Tank], shop: Shop, ship: StarShip) -> bool:
            if not (component in shop.details):
                return False
            if isinstance(component, Engine):
                ship.engine = component
            elif isinstance(component, Tank):
                fuel = ship.tank.fuel if component.capacity <= ship.tank.fuel else component.capacity
                ship.tank = component
                ship.tank.fuel = fuel
            shop.details.remove(component)
            return True

    class InformationModule:
        @staticmethod
        def get_planet_info(planet):
            pass

        @staticmethod
        def get_stock_info(planet):
            pass


planet1 = Planet('Earth')
star_ship1 = StarShip('qwerty', 1000, planet1, Engine(1, 20), Tank(100))
print(star_ship1, star_ship1.cargo_bay.cargo, star_ship1.money)
print(star_ship1.location.stock.products)

star_ship1.make_buy("food", 100)
print(star_ship1, star_ship1.cargo_bay.cargo, star_ship1.money)
print(star_ship1.location.stock.products)

star_ship1.make_sale("food", 200)
print(star_ship1, star_ship1.cargo_bay.cargo, star_ship1.money)
print(star_ship1.location.stock.products)

engine = Engine(10, 1)
planet1.shop.details.append(engine)
star_ship1.buy_new_component(engine)
