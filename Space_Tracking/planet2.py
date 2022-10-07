from random import randint


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
        self.stock = Stock()
        self.shop = Shop()


class Product:
    def __init__(self, title: str):
        self.title = title
        self.price = 0
        self.amount = 0


class Stock:
    def __init__(self):
        self.products = [Product(title) for title in
                         ['mineral', 'medicine', 'food', 'material', 'appliance', 'technic', 'luxury', 'fuel']]
        self.system = Stock.StockSystem(self)

    class StockSystem:
        def __init__(self, stock):
            self.stock = stock

        def update_price(self, product_name: str, price: int):
            self.get_product(product_name).price = price

        def update_amount(self, product_name: str, amount: int):
            self.get_product(product_name).amount = amount

        def get_product(self, product_name: str):
            return [product for product in self.stock.products if product.title == product_name][0]

        # def get_amount_product(self, product_name: str):
        #     return self.get_product(product_name).amount
        #
        # def get_price_product(self, product_name: str):
        #     return self.get_product(product_name).price


class Shop:
    def __init__(self):
        self.tanks = []
        self.engines = []
        self.ships = []
