from random import randint


class Map:
    def __init__(self):
        x = 10
        y = 10
        self.map = [['.'] * x for i in range(y)]

    def check_planet(self, pos_x, pos_y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= pos_x + i < len(self.map[0]) and 0 <= pos_y + j < len(self.map) and not (i == 0 and j == 0) and\
                        self.map[pos_x + i][pos_y + j] != '.':
                    return False
        return True

    def add_planet(self, planet):
        while planet not in self.map:
            pos_x, pos_y = randint(0, 10), randint(0, 10)
            if self.map[pos_x][pos_y] == '.' and self.check_planet(pos_x, pos_y):
                self.map[pos_x][pos_y] = planet


class Player:
    def __init__(self, name=None):
        self.name = name
        self.money = 0
        self.ships = []

    def buy_ship(self, ship, planet):
        pass


class Engine:
    def __init__(self, power=None, weight=None):
        self.power = power
        self.weight = weight


class Tank:
    def __init__(self, capacity=None, weight=None):
        self.capacity = capacity
        self.weight = weight


class StarShip:
    def __init__(self, name: str, capacity: int, location, engine=Engine(), tank=Tank(), player=Player()):
        self.name = name
        self.location = location
        self.engine = engine
        self.tank = tank
        self.player = player
        self.max_capacity = capacity
        self.current_capacity = self.max_capacity

    def distance(self, planet):
        distance = round(((planet.coord[0] ** 2 - self.location.coord[0] ** 2) + (
                planet.coord[1] ** 2 - self.location.coord[1] ** 2)) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        if self.distance > self.tank.capacity:
            print('Вы не можете полететь на эту планету, так как у вас не хватает топлива.')
        elif self.distance <= self.tank.capacity:
            pass

    def refuel(self):
        while self.location.stock.products['Топливо'][0] > 0:
            request = int(input('Сколько топлива вам заправить?\n'))
            if request > self.location.stock.products['Топливо'][0]:
                print(
                    f"{request} топлива нет на складе. На складе {self.location.stock.products['Топливо'][0]} топлива.")
                continue
            else:
                self.location.stock.products['Топливо'][0] -= request
                self.tank.capacity += request
                self.player.money -= self.location.stock.products['Топливо'][1]


class Stock:
    def __init__(self):
        self.products = {'Еда': (0, 0),
                         'Минералы': (0, 0),
                         'Медикаменты': (0, 0),
                         'Материалы': (0, 0),
                         'Топливо': (0, 0),
                         'Бытовая техника': (0, 0),
                         'Промышленная техника': (0, 0),
                         'Предметы роскоши': (0, 0)
                         }  # (0 - кол-во, 0 - цена)

    def increase_products(self, product, quantity):
        self.products[product][0] += quantity
        print(f'The quantity of {product} has increase by {quantity}')

    def new_price(self, product, price):
        self.products[product][1] = price
        print(f'The price of {product} has risen by {price}')


class Shop:
    def __init__(self):
        self.ships = [StarShip]
        self.engines = [Engine]
        self.tanks = [Tank]


class Planet:
    def __init__(self, name: str, planet_type, x: int, y: int):
        self.name = name
        self.planet_type = planet_type
        self.stock = Stock()
        self.coord = (x, y)

    def get_prices(self):
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices
