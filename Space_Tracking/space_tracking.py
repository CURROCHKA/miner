from random import randint


class Map:
    def __init__(self):
        self.n = 10
        self.m = 10
        self.map = [['.'] * self.n for i in range(self.m)]

    def count_planet(self):
        count = 0
        for i in range(self.n):
            for j in range(self.m):
                if self.check_planet(i, j):
                    count += 1
        return count

    def check_planet(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < len(self.map[0]) and 0 <= y + j < len(self.map) and not (i == 0 and j == 0) and \
                        self.map[x + i][y + j] != '.':
                    return False
        return True

    def add_planet(self, planet):
        if self.count_planet() > 1:
            while planet not in [j for i in self.map for j in i]:
                x, y = randint(0, self.n - 1), randint(0, self.m - 1)
                if self.map[x][y] == '.' and self.check_planet(x, y):
                    self.map[x][y] = planet
                    planet.coord = (x, y)
        return False


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

    def get_distance(self, planet):
        distance = round(((planet.coord[0] - self.location.coord[0]) ** 2 + (
                planet.coord[1] - self.location.coord[1]) ** 2) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        distance = self.get_distance(planet)
        if distance > self.tank.capacity:
            print('Вы не можете полететь на эту планету, так как у вас не хватает топлива.')
        elif distance <= self.tank.capacity:
            self.location = planet
            self.tank.capacity -= distance // self.engine.power
            print(f'Вы прибыли на планету {planet.name}')

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
    def __init__(self, name: str, planet_type):
        self.name = name
        self.planet_type = planet_type
        self.stock = Stock()
        self.coord = None

    def get_prices(self):
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices


map_ = Map()
planet_1 = Planet('Auropa', 'None')
planet_2 = Planet('Earth', 'None')
map_.add_planet(planet_1)
map_.add_planet(planet_2)
engine = Engine(1, 50)
tank = Tank(100, 50)
player = Player('Ivan')
star_ship = StarShip('Buran', 100, planet_1, engine, tank, player)
star_ship.move_to_planet(planet_2)

