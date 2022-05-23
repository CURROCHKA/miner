class Player:
    def __init__(self, name):
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

    def __get_distance(self, planet):
        distance = round(((planet.coord[0] - self.location.coord[0]) ** 2 + (
                planet.coord[1] - self.location.coord[1]) ** 2) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        if planet != self.location:
            distance = self.__get_distance(planet)
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

    def increase_products(self, product, quantity):
        self.products[product][0] += quantity

    def new_price(self, product, price):
        self.products[product][1] = price


class Shop:
    def __init__(self):
        self.ships = []
        self.engines = []
        self.tanks = []


class Planet:
    def __init__(self, name: str, planet_type: str, coord):
        self.name = name
        self.planet_type = planet_type
        self.stock = Stock()
        self.shop = Shop()
        self.coord = coord

    def get_prices(self):
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices


planet1 = Planet('Auropa', 'None', (4, 3))
planet2 = Planet('Earth', 'None', (1, 0))
player = Player('Ivan')
engine = Engine(1, 50)
tank = Tank(100, 50)
star_ship = StarShip('Buran', 100, planet2, engine, tank)
