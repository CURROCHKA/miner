from random import randint
from typing import Tuple, List
# from star_ship import Engine, Tank, StarShip

HEIGHT = 10
WIDTH = 10
planets_coord = []


def _generate_coord() -> Tuple[int, int]:
    while True:
        x, y = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)
        if (x, y) not in planets_coord:
            planets_coord.append((x, y))
            return x, y


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.coord = _generate_coord()
        self.stock = Stock()
        self.shop = Shop()


class Stock:
    def __init__(self):
        self.products = {'food': [100, 10],
                         'minerals': [100, 20],
                         'medicines': [100, 30],
                         'materials': [100, 100],
                         'fuel': [1000, 10],
                         'appliances': [100, 50],
                         'technic': [100, 80],
                         'luxuries': [100, 100]
                         }  # (0 - кол-во, 0 - цена)
        self.system = StockSystem(self)


class StockSystem:
    def __init__(self, stock: Stock):
        self.stock = stock

    def update_price(self, product_name: str, price: int):
        self.get_product(product_name)[1] = price

    def update_amount(self, product_name: str, amount: int):
        self.get_product(product_name)[0] = amount

    def get_product(self, product_name: str) -> List[float]:
        return self.stock.products[product_name]


class Shop:
    def __init__(self):
        self.tanks = {}
        self.engines = {}
        # self.engines = {Engine(1): 10)
        self.ships = {}
        self.system = ShopSystem(self)


class ShopSystem:
    def __init__(self, stock: Shop):
        self.stock = stock
        self.tanks = self.stock.tanks
        self.engines = self.stock.engines
        self.ships = self.stock.ships

    def get_price(self, detail) -> float:
        if detail in self.tanks:
            return self.tanks[detail]
        if detail in self.engines:
            return self.engines[detail]
        return self.ships[detail]
