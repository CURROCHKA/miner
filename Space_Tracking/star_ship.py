import json
from player import player

HEIGHT = 10
WIDTH = 10


def read_file():
    with open('game_info.json') as g_i:
        data = json.load(g_i)
    return data


def change_file(*key, value):
    data = read_file()
    if len(key) == 1:
        data[key[0]] = value
    else:
        data[key[0]][key[1]] = value
    with open('game_info.json', 'w') as g_i:
        json.dump(data, g_i)


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

    def number_of_products(self):
        for i in self.cargo:
            print(f'{i.title()}: {self.cargo[i]}')

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
                change_file('location', value=planet.name)
                self.tank.fuel -= distance * self.engine.power
                print(f'Вы прибыли на планету {planet.name}')
        else:
            print('Вы уже находитесь на этой планете.')

    def is_valid_fuel(self, fuel: int) -> bool:
        if type(fuel) is int and fuel >= 0:
            return True
        else:
            print('Введите числовое положительное значение.')
        return False

    def is_possible_refuel(self, fuel: int) -> bool:
        if fuel * self.location.stock.products['fuel'][1] <= player.money:
            if fuel <= self.location.stock.products['fuel'][0]:
                return True
            else:
                print(
                    f"{fuel} топлива нет на складе. На складе {self.location.stock.products['fuel'][0]} "
                    f"топлива."
                )
        else:
            print(f'У вас не хватает денег, чтобы заправить {fuel} топлива.')
        return False

    def refuel(self, fuel: int):
        if self.is_valid_fuel(fuel) and self.is_possible_refuel(fuel):
            if fuel + self.tank.fuel > self.tank.capacity:
                player.money -= (self.tank.capacity - self.tank.fuel) * self.location.stock.products['fuel'][1]
                self.location.stock.products['fuel'][0] -= self.tank.capacity - self.tank.fuel
                print(f'Вы заправили {self.tank.capacity - self.tank.fuel} топлива за '
                      f'{(self.tank.capacity - self.tank.fuel) * self.location.stock.products["fuel"][1]} кредитов')
                self.tank.fuel += self.tank.capacity - self.tank.fuel
                change_file('star_ship_fuel', value=self.tank.fuel)
                change_file('money', value=player.money)
                return True
            else:
                player.money -= self.location.stock.products['fuel'][1] * fuel
                self.location.stock.products['fuel'][0] -= fuel
                self.tank.fuel += fuel
                change_file('star_ship_fuel', value=self.tank.fuel)
                change_file('money', value=player.money)
                print(f'Вы заправили {fuel} топлива за {self.location.stock.products["fuel"][1] * fuel} кредитов')
                return True
        return False

    def is_valid_product_b(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int and amount >= 0:
                return True
            else:
                print('Введите числовое положительное значение.')
        else:
            print('Такого продукта нет.')
        return False

    def is_possible_buy(self, product: str, amount: int) -> bool:
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
        if self.is_valid_product_b(product, amount) and self.is_possible_buy(product, amount):
            if self.current_capacity + amount > self.capacity:
                player.money -= (self.capacity - self.current_capacity) * self.location.stock.products[product][1]
                self.location.stock.products[product][0] -= self.capacity - self.current_capacity
                self.cargo[product] += self.capacity - self.current_capacity
                print(f'Вы купили {self.capacity - self.current_capacity} {product} за '
                      f'{(self.capacity - self.current_capacity) * self.location.stock.products[product][1]}')
                change_file('cargo', product, value=self.cargo[product])
                change_file('money', value=player.money)
                return True
            else:
                player.money -= self.location.stock.products[product][1] * amount
                self.location.stock.products[product][0] -= amount
                self.cargo[product] += amount
                print(f'Вы купили {amount} {product} за {self.location.stock.products[product][1] * amount}')
                change_file('cargo', product, value=self.cargo[product])
                change_file('money', value=player.money)
                return True
        return False

    def is_valid_product_s(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int and amount >= 0:
                return True
            else:
                print('Введите числовое положительное значение.')
        else:
            print('Такого продукта нет.')
        return False

    def sale(self, product: str, amount: int):
        if self.is_valid_product_s(product, amount):
            if self.cargo[product] >= amount:
                self.cargo[product] -= amount
                self.location.stock.products[product][0] += amount
                player.money += self.location.stock.products[product][1] * amount
                change_file('cargo', product, value=self.cargo[product])
                change_file('money', value=player.money)
                print(f'Вы продали {amount} {product} за {self.location.stock.products[product][1] * amount} кредитов.')
                return True
            else:
                print(f'У вас есть только {self.cargo[product]} {product.lower()}')
        return False
