import json
import sys

from player import player
from settings import Settings
import time

settings = Settings()


def read_file() -> dict:
    with open('game_info.json') as g_i:
        data = json.load(g_i)
    return data


def change_file(key: str, value: any):
    data = read_file()
    data[key] = value
    with open('game_info.json', 'w') as g_i:
        json.dump(data, g_i)


def is_training() -> bool:
    while True:
        print('Пройти обучение: Y', 'Не проходить обучение: N', sep='\n')
        string = input().lower()
        if string == 'y':
            return True
        elif string == 'n':
            return False


def training(star_ship):
    print(f'Добро пожаловать, {player.name}!\n'
          f'В начале игры вам доступен {star_ship.name}.')
    time.sleep(2)
    print('Давай заправимся.')
    while not star_ship.refuel(int(input('Введите кол-во топлива, которое хотите заправить: '))):
        continue
    print('Заправляемся...')
    time.sleep(3)
    print('Теперь - купим продукты, чтобы продать их на другой планете.')
    time.sleep(2)
    print(f'У вас {player.money} денег.')
    time.sleep(2)
    print('Список продуктов:')
    star_ship.location.stock.product_list()
    while not star_ship.buy(input('Введите название продукта, который хотели бы купить: '),
                            int(input('И его кол-во: '))):
        continue


def interface(status: dict, star_ship):
    if status['new_game']:
        if is_training():
            training(star_ship)
    change_file('new_game', False)
    print()
    print('1. Заправиться.', '2. Купить продукты.', '3. Продать продукты. ', '4. Отправиться на другую планету.',
          '5. Посмотреть статистику игры.', '6. Выход из игры.',
          sep='\n')
    print()
    req = int(input())
    if req == 1:
        while not star_ship.refuel(int(input('Введите кол-во топлива, которое хотите заправить: '))):
            continue
    elif req == 2:
        star_ship.location.stock.product_list()
        while not star_ship.buy(input('Введите название продукта, который хотели бы купить: '),
                                int(input('И его кол-во: '))):
            continue
    elif req == 3:
        star_ship.location.stock.product_list()
        while not star_ship.sale(input('Введите название продукта, который хотели бы продать: '),
                                 int(input('И его кол-во: '))):
            continue
    elif req == 4:
        print('1. Посмотреть цены на продукты на других планетах.', '2. Посмотреть расстояние до планет.',
              '3. Выбор планеты, на которую вы полетите.', '4. Вернуться на прошлую страницу.', sep='\n')
        print()
        req1 = int(input())
        if req1 == 1:
            for planet in settings.planets:
                if planet == star_ship.location:
                    print(f'Планета {planet.name} - вы здесь')
                else:
                    print(f'Планета {planet.name}')
                planet.stock.product_list()
        elif req1 == 2:
            for planet in settings.planets:
                if planet != star_ship.location:
                    print(
                        f'От планеты {star_ship.location.name} до планеты {planet.name} {star_ship.get_distance(planet)}')
            print()
        elif req1 == 3:
            for planet in settings.planets:
                if planet != star_ship.location:
                    print(planet.name)
            print()
            planet = input('Введите название планеты, на которую хотите полететь.\n')
            print()
            for i in settings.planets:
                if planet.lower() == i.name.lower():
                    star_ship.move_to_planet(i)
            print()
        elif req1 == 4:
            interface(status, star_ship)
    elif req == 5:
        print(f'Вы находитесь на планете {star_ship.location.name}\n\nУ вас {player.money} кредитов\n\n{star_ship.number_of_products()}\n{star_ship.capacity - star_ship.current_capacity} свободного места в грузовом отсеке.\n\n{star_ship.tank.fuel} топлива.\n')
    elif req == 6:
        sys.exit()


def new_game():
    planets = settings.planets
    star_ship = settings.star_ships[0]
    change_file('planets_coord', [planet.coord for planet in planets])
    change_file('star_ship_name', star_ship.name)
    change_file('location', planets[0].name)
    change_file('star_ship_fuel', 0)
    change_file('cargo', {"minerals": 0, "medicines": 0, "food": 0, "materials": 0, "appliances": 0, "technic": 0,
                          "luxuries": 0})
    change_file('money', 10000)
    return star_ship


def is_new_game() -> tuple or bool:
    while True:
        print('Новая игра: Y', 'Продолжить игру: C', 'Завершить игру: N', sep='\n')
        string = input().lower()
        if string == 'y':
            change_file('new_game', True)
            star_ship = new_game()
            return True, star_ship
        elif string == 'c':
            star_ship = None
            change_file('new_game', False)
            for i in range(len(settings.star_ships)):
                if settings.star_ships[i].name == read_file()['star_ship_name']:
                    star_ship = settings.star_ships[i]
            for i in range(len(settings.planets)):
                settings.planets[i].coord = read_file()['planets_coord'][i]
            for i in range(len(settings.planets)):
                if settings.planets[i].name == read_file()['location']:
                    star_ship.location = settings.planets[i]
            star_ship.tank.fuel = read_file()['star_ship_fuel']
            star_ship.cargo = read_file()['cargo']
            return True, star_ship
        elif string == 'n':
            return False, None


def main():
    flag, star_ship = is_new_game()
    while flag:
        interface(read_file(), star_ship)


main()
