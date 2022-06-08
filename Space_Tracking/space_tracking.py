from random import randint

HEIGHT = 10
WIDTH = 10


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
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 0,
                      'materials': 0,
                      'appliances': 0,
                      'technic': 0,
                      'luxuries': 0
                      }

    @property
    def current_capacity(self) -> int:
        return sum(self.cargo.values())

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

    def __is_valid_fuel(self, fuel: int) -> bool:
        if type(fuel) is int:
            if fuel > 0:
                return True
            else:
                print('Введите положительное значение.')
        else:
            print('Введите числовое значение.')
        return False

    def __is_possible_refuel(self, fuel: int) -> bool:
        if fuel * self.location.stock.products['fuel'][1] <= player.money:
            if fuel <= self.location.stock.products['fuel'][0]:
                return True
            else:
                print(
                    f"{fuel} топлива нет на складе. На складе {self.location.stock.products['Fuel'][0]} "
                    f"топлива."
                )
        else:
            print(f'У вас не хватает денег, чтобы заправить {fuel} топлива.')
        return False

    def refuel(self, fuel: int):
        if self.__is_valid_fuel(fuel) and self.__is_possible_refuel(fuel):
            if fuel + self.tank.fuel > self.tank.capacity:
                player.money -= (self.tank.capacity - self.tank.fuel) * self.location.stock.products['fuel'][1]
                self.location.stock.products['fuel'][0] -= self.tank.capacity - self.tank.fuel
                self.tank.fuel += self.tank.capacity - self.tank.fuel
            else:
                player.money -= self.location.stock.products['fuel'][1] * fuel
                self.location.stock.products['fuel'][0] -= fuel
                self.tank.fuel += fuel

    def __is_valid_product_b(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int:
                if amount > 0:
                    return True
                else:
                    print('Введите положительное значение.')
            else:
                print('Введите числовое значение.')
        else:
            print('Такого продукта нет.')
        return False

    def __is_possible_buy(self, product: str, amount: int) -> bool:
        if self.location.stock.products[product][0] >= amount:
            if player.money >= self.location.stock.products[product][1] * amount:
                return True
            else:
                print(f'У вас не хватает денег, чтобы купить {amount} {product.lower()}.')
        else:
            print(f'{amount} {product.lower()} нет на складе. На складе '
                  f'{self.location.stock.products[product][0]} {product.lower()}')
        return False

    def buy(self, product: str, amount: int):
        if self.__is_valid_product_b(product, amount) and self.__is_possible_buy(product, amount):
            if self.current_capacity + amount > self.capacity:
                player.money -= (self.capacity - self.current_capacity) * self.location.stock.products[product][1]
                self.location.stock.products[product][0] -= self.capacity - self.current_capacity
                self.cargo += self.capacity - self.current_capacity
            else:
                player.money -= self.location.stock.products[product][1] * amount
                self.location.stock.products[product][0] -= amount
                self.cargo[product] += amount

    def __is_valid_product_s(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int:
                if amount > 0:
                    return True
                else:
                    print('Введите положительное значение.')
            else:
                print('Введите числовое значение.')
        else:
            print('Такого продукта нет.')
        return False

    def sale(self, product: str, amount: int):
        if self.__is_valid_product_s(product, amount):
            if self.cargo[product] >= amount:
                self.cargo[product] -= amount
                self.location.stock.products[product][0] += amount
                player.money += self.location.stock.products[product][1] * amount
            else:
                print(f'У вас есть только {self.cargo[product]} {product.lower()}')


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
    def __init__(self, name: str, planet_type: str):
        self.name = name
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
print(planet2.stock.products['fuel'], 'Топливо на складе')
star_ship.refuel(1000)
print(player.money)
print(planet2.stock.products['fuel'], 'Топливо на складе')
print(star_ship.tank.fuel, 'Топливо')
print(star_ship.get_distance(planet1), 'Расстояние')
star_ship.move_to_planet(planet1)
print(star_ship.tank.fuel, 'Топливо после перелёта на др. планету')
star_ship.refuel(10)
print(star_ship.tank.fuel, 'Топливо после заправки')
print(planet1.stock.products['fuel'], 'Топливо на складе')
print(planet1.stock.products['food'], 'Еда на складе')
print(player.money, 'Деньги игрока')
print(star_ship.cargo['food'], 'Еда у игрока')
star_ship.buy('food', 10)
print('Купил еду')
print(player.money, 'Деньги игрока после покупки еды')
print(planet1.stock.products['food'], 'Еда на складе после покупки')
print(star_ship.cargo['food'], 'Еда у игрока после покупки')
star_ship.sale('food', 10)
print('Продал еду')
print(planet1.stock.products['food'], 'Еда на складе после продажи')
print(star_ship.cargo['food'], 'Еда у игрока после продажи')
print(player.money, 'Деньги игрока после продажи еды')
