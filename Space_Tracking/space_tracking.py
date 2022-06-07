from random import randint

ROWS = 10  # Кол-во строк
COLUMNS = 10  # Кол-во столбцов


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 2000000

    def buy_ship(self, ship, planet):
        pass


class Engine:
    def __init__(self, power: int, weight: int):
        self.power = power
        self.weight = weight


class Tank:
    def __init__(self, capacity: int, weight: int):
        self.capacity = capacity
        self.fuel = 0
        self.weight = weight


class StarShip:
    def __init__(self, name: str, capacity: int, location, engine, tank):
        self.name = name
        self.location = location
        self.engine = engine
        self.tank = tank
        self.capacity = capacity
        self.cargo = {'Minerals': 0,
                      'Medicines': 0,
                      'Food': 0,
                      'Materials': 0,
                      'Appliances': 0,
                      'Technic': 0,
                      'Luxuries': 0
                      }

    @property
    def current_capacity(self) -> int:
        return sum([self.cargo.values()])

    def get_distance(self, planet) -> int:
        distance = round(((planet.coord[0] - self.location.coord[0]) ** 2 + (
                planet.coord[1] - self.location.coord[1]) ** 2) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        if planet != self.location:
            distance = self.get_distance(planet)
            if distance * self.engine.power > self.tank.fuel:
                print('Вы не можете полететь на эту планету, так как у вас не хватает топлива.')
            elif distance * self.engine.power <= self.tank.fuel:
                self.location = planet
                self.tank.fuel -= distance * self.engine.power
                print(f'Вы прибыли на планету {planet.name}')
        else:
            print('Вы уже находитесь на этой планете.')

    def refuel(self, fuel: int):
        if type(fuel) is int:
            if fuel > 0:
                if fuel * self.location.stock.products['Fuel'][1] <= player.money:
                    if fuel <= self.location.stock.products['Fuel'][0]:
                        if fuel + self.tank.fuel > self.tank.capacity:
                            self.tank.fuel += self.tank.capacity - self.tank.fuel
                        else:
                            self.tank.fuel += fuel
                        self.location.stock.products['Fuel'][0] -= fuel
                        player.money -= self.location.stock.products['Fuel'][1] * fuel
                    else:
                        print(
                            f"{fuel} топлива нет на складе. На складе {self.location.stock.products['Fuel'][0]} "
                            f"топлива."
                        )
                else:
                    print(f'У вас не хватает денег, чтобы заправить {fuel} топлива.')
            else:
                print('Введите положительное значение.')
        else:
            print('Введите числовое значение.')

    def buy(self, product: str, amount: int):
        if product.title() in self.cargo:
            product = product.title()
            if type(amount) is int:
                if amount > 0:
                    if self.location.stock.products[product][0] > 0:
                        if self.location.stock.products[product][0] >= amount:
                            if player.money >= self.location.stock.products[product][1] * amount:
                                self.location.stock.products[product][0] -= amount
                                self.cargo[product] += amount
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
        if product.title() in self.cargo:
            product = product.title()
            if type(amount) is int:
                if amount > 0:
                    if self.cargo[product] >= amount:
                        self.cargo[product] -= amount
                        self.location.stock.products[product][0] += amount
                        player.money += self.location.stock.products[product][1] * amount
                    else:
                        print(f'У вас есть только {self.cargo[product]} {product.lower()}')
                else:
                    print('Введите положительное значение.')
            else:
                print('Введите числовое значение.')
        else:
            print('Такого продукта нет.')


class Stock:
    def __init__(self):
        self.products = {'Food': [100, 10],
                         'Minerals': [1000, 20],
                         'Medicines': [100, 30],
                         'Materials': [100, 100],
                         'Fuel': [1000, 10],
                         'Appliances': [100, 50],
                         'Technic': [100, 80],
                         'Luxuries': [100, 100]
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

    def __count_planets(self) -> int:
        count = 0
        for i in range(ROWS):
            for j in range(COLUMNS):
                if [i, j] not in planets_coord:
                    count += 1
        return count

    def __generate_coord(self) -> tuple:
        while self.__count_planets() <= ROWS * COLUMNS:
            x, y = randint(0, ROWS - 1), randint(0, COLUMNS - 1)
            if [x, y] in planets_coord:
                continue
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
engine = Engine(2, 50)
tank = Tank(100, 50)
star_ship = StarShip('Buran', 100, planet2, engine, tank)
print(star_ship.tank.fuel, 'Топливо')
print(player.money)
print(planet2.stock.products['Fuel'], 'Топливо на складе')
star_ship.refuel(1000)
print(player.money)
print(planet2.stock.products['Fuel'], 'Топливо на складе')
print(star_ship.tank.fuel, 'Топливо')
print(star_ship.get_distance(planet1), 'Расстояние')
star_ship.move_to_planet(planet1)
print(star_ship.tank.fuel, 'Топливо после перелёта на др. планету')
star_ship.refuel(10)
print(star_ship.tank.fuel, 'Топливо после заправки')
print(planet1.stock.products['Fuel'], 'Топливо на складе')
print(planet1.stock.products['Food'], 'Еда на складе')
print(player.money, 'Деньги игрока')
print(star_ship.cargo['Food'], 'Еда у игрока')
star_ship.buy('food', 10)
print('Купил еду')
print(player.money, 'Деньги игрока после покупки еды')
print(planet1.stock.products['Food'], 'Еда на складе после покупки')
print(star_ship.cargo['Food'], 'Еда у игрока после покупки')
star_ship.sale('food', 1)
print('Продал еду')
print(planet1.stock.products['Food'], 'Еда на складе после продажи')
print(star_ship.cargo['Food'], 'Еда у игрока после продажи')
print(player.money, 'Деньги игрока после продажи еды')
