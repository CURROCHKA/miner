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

    def move(self, planet):
        print(f'Movement from {self.location} to {planet}')

    def refuel(self):
        while self.location.stock.products['Топливо'][0] > 0:
            request = int(input('Сколько топлива вам заправить?\n'))
            if request > self.location.stock.products['Топливо'][0]:
                print(f"{request} топлива нет на складе. На складе {self.location.stock.products['Топливо'][0]} топлива.")
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


class Planet:
    def __init__(self, name, planet_type):
        self.name = name
        self.planet_type = planet_type
        self.stock = Stock()

    def get_prices(self):
        prices = {}
        for i in self.stock.products:
            prices.update({i: self.stock.products[i][1]})
        return prices


planet = Planet('Earth', 'asasqwq')
print(planet.get_prices())
