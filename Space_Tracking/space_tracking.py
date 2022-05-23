from random import randint


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 2000
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
    def __init__(self, name: str, capacity: int, location, engine=Engine(), tank=Tank()):
        self.name = name
        self.location = location
        self.engine = engine
        self.tank = tank
        self.max_capacity = capacity
        self.current_capacity = self.max_capacity

    def get_distance(self, planet) -> int:
        distance = round(((planet.coord[0] - self.location.coord[0]) ** 2 + (
                planet.coord[1] - self.location.coord[1]) ** 2) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        if planet != self.location:
            distance = self.get_distance(planet)
            if distance > self.tank.capacity:
                print('Вы не можете полететь на эту планету, так как у вас не хватает топлива.')
            elif distance <= self.tank.capacity:
                self.location = planet
                self.tank.capacity -= distance // self.engine.power
                print(f'Вы прибыли на планету {planet.name}')
        else:
            print('Вы уже находитесь на этой планете.')

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
                player.money -= self.location.stock.products['Топливо'][1] * request
                break


class Stock:
    def __init__(self):
        self.products = {'Еда': [0, 0],
                         'Минералы': [0, 0],
                         'Медикаменты': [0, 0],
                         'Материалы': [0, 0],
                         'Топливо': [100, 10],
                         'Бытовая техника': [0, 0],
                         'Промышленная техника': [0, 0],
                         'Предметы роскоши': [0, 0]
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
    def __init__(self, name: str, planet_type: str):
        self.name = name
        self.planet_type = planet_type
        self.stock = Stock()
        self.shop = Shop()
        self.coord = self.__generate_coord()

    def __count_freespace(self) -> int:
        count = 0
        for i in range(10):
            for j in range(10):
                if not self.__check_planets(i, j):
                    count += 1
        return count

    def __check_planets(self, x: int, y: int) -> bool:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < 10 and 0 <= y + j < 10 and not (i == 0 and j == 0) \
                        and [x + i, y + j] in planets_coord:
                    return True
        return False

    def __generate_coord(self) -> tuple:
        if self.__count_freespace() > 1:
            while True:
                x, y = randint(0, 9), randint(0, 9)
                if [x, y] in planets_coord:
                    continue
                if not self.__check_planets(x, y):
                    planets_coord.append([x, y])
                    return x, y

    def get_prices(self) -> dict:
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices


planets_coord = []
planet1 = Planet('Auropa', 'None')
planet2 = Planet('Earth', 'None')
planet3 = Planet('Mars', 'None')
player = Player('Ivan')
engine = Engine(1, 50)
tank = Tank(100, 50)
star_ship = StarShip('Buran', 100, planet2, engine, tank)
