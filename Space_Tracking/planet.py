from random import randint


HEIGHT = 10
WIDTH = 10
planets_coord = []


class Stock:
    def __init__(self):
        self.products = {'food': [100, 10],
                         'minerals': [1000, 20],
                         'medicines': [100, 30],
                         'materials': [100, 100],
                         'fuel': [1000, 10],
                         'appliances': [100, 50],
                         'technic': [100, 80],
                         'luxuries': [100, 100]
                         }  # (0 - кол-во, 0 - цена)

    def increase_products(self, product: str, quantity: int):
        self.products[product][0] += quantity

    def new_price(self, product: str, price: int):
        self.products[product][1] = price


class Shop:
    def __init__(self):
        self.ships = []
        self.engines = []
        self.tanks = []


class Planet:
    def __init__(self, id: str, planet_type: str):
        self.id = id
        self.planet_type = planet_type
        self.stock = Stock()
        self.shop = Shop()
        self.coord = self.__generate_coord()

    def __count_planets(self) -> int:
        count = 0
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if [i, j] not in planets_coord:
                    count += 1
        return count

    def __generate_coord(self) -> tuple:
        while self.__count_planets() <= HEIGHT * WIDTH:
            x, y = randint(0, HEIGHT - 1), randint(0, WIDTH - 1)
            if [x, y] in planets_coord:
                continue
            planets_coord.append([x, y])
            return x, y

    def get_prices(self) -> dict:
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices
