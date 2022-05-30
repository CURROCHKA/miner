from random import randint

N, M = 10, 10


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 2000

    def buy_ship(self, ship, planet):
        pass


class Engine:
    def __init__(self, power=None, weight=None):
        self.power = power
        self.weight = weight


class Tank:
    def __init__(self, capacity=None, weight=None):
        self.capacity = capacity
        self.fuel = self.capacity
        self.weight = weight


class StarShip:
    def __init__(self, name: str, capacity: int, location, engine=Engine(), tank=Tank()):
        self.name = name
        self.location = location
        self.engine = engine
        self.tank = tank
        self.capacity = capacity
        self.compartment = {'Минералы': 0,
                            'Медикаменты': 0,
                            'Еда': 0,
                            'Материалы': 0,
                            'Бытовая техника': 0,
                            'Промышленная техника': 0,
                            'Предметы роскоши': 0
                            }
        self.current_capacity = sum([self.compartment[i] for i in self.compartment])

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
                self.tank.fuel -= distance * self.engine.power
                print(f'Вы прибыли на планету {planet.name}')
        else:
            print('Вы уже находитесь на этой планете.')

    def refuel(self, fuel: int):
        if type(fuel) is int:
            if fuel * self.location.stock.products['Топливо'][1] <= player.money:
                if fuel > 0:
                    if fuel > self.location.stock.products['Топливо'][0]:
                        print(
                            f"{fuel} топлива нет на складе. На складе {self.location.stock.products['Топливо'][0]} "
                            f"топлива."
                        )
                    else:
                        if fuel + self.tank.fuel > self.tank.capacity:
                            self.tank.fuel += self.tank.capacity - self.tank.fuel
                        else:
                            self.tank.fuel += fuel
                        self.location.stock.products['Топливо'][0] -= fuel
                        player.money -= self.location.stock.products['Топливо'][1] * fuel
                else:
                    print('Введите положительное значение.')
            else:
                print(f'У вас не хватает денег, чтобы заправить {fuel} топлива.')
        else:
            print('Введите числовое значение.')

    def buy(self, product: str, amount: int):
        if product.title() in self.compartment:
            product = product.title()
            if type(amount) is int:
                if amount > 0:
                    if self.location.stock.products[product][0] > 0:
                        if self.location.stock.products[product][0] >= amount:
                            if player.money >= self.location.stock.products[product][1] * amount:
                                self.location.stock.products[product][0] -= amount
                                self.compartment[product] += amount
                                player.money -= self.location.stock.products[product][1] * amount
                            else:
                                print(f'У вас не хватает денег, чтобы купить {amount} {product.lower()}.')
                        else:
                            print(f'{amount} {product.lower()} нет на складе. На складе '
                                  f'{self.location.stock.products[product][0]} {product.lower()}')
                    else:
                        print(f'Товар {product.lower()} закончился.')
                else:
                    print('Введите положительное значение.')
            else:
                print('Введите числовое значение.')
        else:
            print('Такого продукта нет.')

    def sale(self, product: str, amount: int):
        if product.title() in self.compartment:
            product = product.title()
            if type(amount) is int:
                if amount > 0:
                    if self.compartment[product] >= amount:
                        self.compartment[product] -= amount
                        self.location.stock.products[product][0] += amount
                        player.money += self.location.stock.products[product][1] * amount
                    else:
                        print(f'У вас есть только {self.compartment[product]} {product.lower()}')
                else:
                    print('Введите положительное значение.')
            else:
                print('Введите числовое значение.')
        else:
            print('Такого продукта нет.')


class Stock:
    def __init__(self):
        self.products = {'Еда': [100, 10],
                         'Минералы': [1000, 20],
                         'Медикаменты': [100, 30],
                         'Материалы': [100, 100],
                         'Топливо': [1000, 10],
                         'Бытовая техника': [100, 50],
                         'Промышленная техника': [100, 80],
                         'Предметы роскоши': [100, 100]
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
        for i in range(N):
            for j in range(M):
                if not self.__check_planets(i, j):
                    count += 1
        return count

    def __check_planets(self, x: int, y: int) -> bool:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < N and 0 <= y + j < M and not (i == 0 and j == 0) \
                        and [x + i, y + j] in planets_coord:
                    return True
        return False

    def __generate_coord(self) -> tuple:
        if self.__count_freespace() > 1:
            while True:
                x, y = randint(0, N - 1), randint(0, M - 1)
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
print(star_ship.tank.fuel, 'Топливо')
star_ship.move_to_planet(planet1)
print(star_ship.tank.fuel, 'Топливо после перелёта на др. планету')
star_ship.refuel(10)
print(star_ship.tank.fuel, 'Топливо после заправки')
print(planet1.stock.products['Топливо'], 'Топливо на складе')
print(planet1.stock.products['Еда'], 'Еда на складе')
print(player.money, 'Деньги игрока')
print(star_ship.compartment['Еда'], 'Еда у игрока')
star_ship.buy('еда', 10)
print('Купил еду')
print(player.money, 'Деньги игрока после покупки еды')
print(planet1.stock.products['Еда'], 'Еда на складе после покупки')
print(star_ship.compartment['Еда'], 'Еда у игрока после покупки')
star_ship.sale('еда', 1)
print('Продал еду')
print(planet1.stock.products['Еда'], 'Еда на складе после продажи')
print(star_ship.compartment['Еда'], 'Еда у игрока после продажи')
print(player.money, 'Деньги игрока после продажи еды')
