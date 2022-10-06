from random import randint
from product import Product


HEIGHT = 10
WIDTH = 10
planets_coord = []


def generate_coord() -> tuple:
    while True:
        x, y = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)
        if (x, y) not in planets_coord:
            planets_coord.append((x, y))
            return x, y


class Planet:
    def __init__(self, name: str):
        self.name = name
        self.coord = generate_coord()


class Stock:
    def __init__(self):
        self.products = [Product(title) for title in
                         ['mineral', 'medicine', 'food', 'material', 'appliance', 'technic', 'luxury', 'fuel']]
        self.system = Stock.StockSystem(self)

    class StockSystem:
        def __init__(self, stock):
            self.stock = stock

        def update_price(self, product, price):
            self.stock.products[product].price = price

        def update_amount(self, product, amount):
            self.stock.products[product].amount = amount


class Shop:
    def __init__(self):
        self.tanks = []
        self.engines = []
        self.ships = []

