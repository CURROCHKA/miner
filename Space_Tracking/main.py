from planet import Planet
from star_ship import StarShip, Engine, Tank
from prettytable import PrettyTable
from time import sleep
import re
from typing import Union, Tuple


def game_loop():
    while True:
        print_ships()
        print('Enter the "Next" ot "Next # (the number of moves you want to skip)" command to skip the move')
        ship = input('Enter a number of the ship you want to interact with (or quit the game - 0): ')
        if ship == '0':
            break
        if 'next' in ship:
            skip_move(ship)
            continue
        ship = identify_ship(ship)
        if ship is None:
            continue
        ship_activities(ship)


def skip_move(command: str):
    moves = re.findall(r'\d+', command)
    if len(moves) == 1:
        moves = int(moves[0])
    else:
        moves = 1

    for ship in context['ships']:
        if ship.inactivity_moves - moves >= 0:
            ship.inactivity_moves -= moves
        else:
            ship.inactivity_moves = 0


def identify_ship(number_ship: str) -> Union[None, StarShip]:
    try:
        number_ship = int(number_ship)
        if number_ship < 0 or number_ship > len(context['ships']):
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            return None
    except ValueError:
        print('\nEnter a positive integer\n')
        sleep(1)
        return None

    ship = context['ships'][number_ship - 1]
    if ship.inactivity_moves == 0:
        return ship


def ship_activities(ship: StarShip):
    while True:
        print_activities()

        flag, player_input = correct_int_input('Choose activity (Number): ')
        if not flag:
            ship_activities(ship)
            break
        elif player_input == 0:
            break
        elif player_input >= 6:
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            ship_activities(ship)
            break
        elif player_input == 1:
            refuel(ship)
        elif player_input == 2:
            buy_products(ship)
        elif player_input == 3:
            sale_products(ship)
        elif player_input == 4:
            buy_components(ship)
        elif player_input == 5:
            if list_of_planets(ship):
                break


def correct_int_input(msg: str) -> Union[Tuple[bool, int], Tuple[bool, None]]:
    try:
        inp = int(input(msg))
    except ValueError:
        print('\nEnter a positive integer\n')
        sleep(1)
        return False, None
    if inp >= 0:
        return True, inp
    print('\nEnter a positive integer\n')
    sleep(1)
    return False, None


def get_products(ship: StarShip):
    stock_products = ship.location.stock.products
    products = {}
    for i, p in enumerate(stock_products):
        products.update({i + 1: p})
    return products


def refuel(ship: StarShip):
    while True:
        flag, fuel = correct_int_input('Enter the units of fuel you want (or choose another activity - 0): ')
        if not flag:
            refuel(ship)
            break
        elif fuel == 0:
            break
        ship.make_refuel(fuel)
        sleep(2)
        break


def buy_products(ship: StarShip):
    products = get_products(ship)
    while True:
        print_products(ship, products)

        flag, num_product = correct_int_input('Enter a number of the product you want to buy (or choose another '
                                              'activity - 0): ')
        if not flag:
            buy_products(ship)
            break
        elif num_product == 0:
            break

        flag, amount = correct_int_input('Enter the amount of the product you want to buy (or choose another activity '
                                         '- 0): ')
        if not flag:
            buy_products(ship)
            break
        elif amount == 0:
            break

        if num_product in products.keys() and amount > 0:
            ship.make_buy(products[num_product], amount)
            sleep(2)
            buy_products(ship)
            break
        else:
            print('There is no such product in the list')
            sleep(1)


def sale_products(ship: StarShip):
    products = get_products(ship)
    while True:
        print_products(ship, products)
        flag, num_product = correct_int_input(
            'Enter a number of the product you want to sale (or choose another activity - 0): ')

        if not flag:
            sale_products(ship)
            break
        elif num_product == 0:
            break

        flag, amount = correct_int_input('Enter the amount of the product you want to sale (or choose another '
                                         'activity - 0): ')

        if not flag:
            sale_products(ship)
            break
        elif amount == 0:
            break

        cargo = ship.cargo_bay.cargo
        if num_product > len(cargo):
            sale_products(ship)
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            break

        product = products[num_product]
        if product in cargo and amount > 0:
            ship.make_sale(product, amount)
            sleep(2)
            sale_products(ship)
            break
        else:
            print('There is no such product in the list')
            sleep(1)


def buy_components(ship: StarShip):
    shop_components = ship.location.shop.components
    components = {}
    for i, c in enumerate(shop_components):
        components.update({i + 1: c})
    while True:
        print_components(ship, components)

        flag, num_component = correct_int_input('Enter a number of the component you want to buy (or choose another '
                                                'activity - 0): ')
        if not flag:
            buy_components(ship)
            break
        elif num_component == 0:
            break

        if num_component > len(components):
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            buy_components(ship)
            break

        component = components[num_component]
        if component in shop_components:
            ship.buy_new_component(component)
            sleep(2)
            buy_components(ship)
            break


def list_of_planets(ship: StarShip) -> bool:
    planets = {}
    for i, planet in enumerate(context['planets']):
        planets.update({i + 1: planet})
    while True:
        print_planets(ship)

        flag, num_planet = correct_int_input('Enter a number of the planet you want to move or check stats (or choose '
                                             'another activity - 0): ')

        if not flag:
            list_of_planets(ship)
            break
        elif num_planet == 0:
            break

        if num_planet > len(planets):
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            list_of_planets(ship)
            break
        planet = planets[num_planet] if planets[num_planet] is not ship.location else planets[num_planet + 1]
        if planet_activities(ship, planet):
            return True


def planet_activities(ship: StarShip, planet: Planet) -> bool:
    while True:
        print_planet_activities(planet)

        flag, player_input = correct_int_input('Choose activity (Number): ')

        if not flag:
            planet_activities(ship, planet)
            break
        elif player_input == 0:
            break
        elif player_input >= 3:
            print('\nEnter a positive integer that you can see in the list\n')
            sleep(1)
            planet_activities(ship, planet)
            break
        elif player_input == 1:
            planet_stats(ship, planet)
        elif player_input == 2:
            if ship.move_to_planet(planet):
                sleep(1)
                return True
            sleep(1)


def planet_stats(ship: StarShip, planet: Planet):
    while True:
        print_planet_stats(ship, planet)
        flag, player_input = correct_int_input('Choose another activity - 0: ')

        if not flag:
            planet_stats(ship, planet)
            break
        elif player_input == 0:
            break


def print_planet_stats(ship: StarShip, planet: Planet):
    table = PrettyTable(['Stats', 'Value', 'Cost'])
    stats = ['Food', 'Minerals', 'Medicines', 'Materials', 'Fuel', 'Appliances', 'Machinery', 'Luxuries']
    products = planet.stock.products
    for stat in stats:
        product_amount, product_cost = products[stat.lower()]
        table.add_row([stat, product_amount, product_cost])
    current_planet = ship.location
    distance = ship.ship_system.NavigationModule.get_distance(current_planet, planet)
    table.add_row(['Distance', distance, '-'])
    print(table)


def print_planet_activities(planet: Planet):
    table = PrettyTable(['Number', 'Activity'], title=planet.name, align='l')
    activities = ['Stats', 'Move to planet']
    for n, activity in enumerate(activities):
        table.add_row([n + 1, activity])
    table.add_row([0, 'Exit'])
    print(table)


def print_products(ship: StarShip, products: dict):
    table = PrettyTable(['Number', 'Product', 'Stock Amount', 'Your amount', 'Price'],
                        title='Products',
                        align='l',
                        padding_width=2)
    stock_products = ship.location.stock.products
    for num_product in products:
        if products[num_product] != 'fuel':
            product = products[num_product]
            stock_amount, price = stock_products[product]
            ship_amount = ship.cargo_bay.cargo[product]
            table.add_row([num_product, product.title(), stock_amount, ship_amount, price])
    print(table)


def print_components(ship: StarShip, components: dict):
    table = PrettyTable(
        ['Number', 'Component', 'Parameters', 'Parameters of your ship', 'Price', 'Price your components',
         'Total cost'],
        title='Components',
        align='l')
    for num_component in components:
        component = components[num_component]
        component_name = component.__class__.__name__
        ship_parameter = f'Speed {ship.engine.speed}' if component_name == 'Engine' else f'Volume {ship.tank.capacity}'
        component_parameter = f'Speed {component.speed}' if component_name == 'Engine' else f'Volume {component.capacity}'
        price = component.price
        ship_price = ship.engine.price if component_name == 'Engine' else ship.tank.price
        total_cost = abs(price - ship_price)
        table.add_row(
            [num_component, component_name, component_parameter, ship_parameter, price, ship_price, total_cost])
    print(table)


def print_planets(ship: StarShip):
    table = PrettyTable(['Number', 'Planet'],
                        title='Planets',
                        align='l')
    num = -1
    for i, planet in enumerate(context['planets']):
        if planet is not ship.location:
            table.add_row([i + 1 if num == -1 else i, planet.name])
        else:
            num = i
    print(table)


def print_ships():
    table = PrettyTable(['Number', 'Ship', 'Status'],
                        align='l')
    for n, ship in enumerate(context['ships']):
        status = f'{ship.inactivity_moves} moves remaining for "Active"' if ship.inactivity_moves > 0 else 'Active'
        table.add_row([n + 1, ship.name, status])
    print(table)


def print_activities():
    table = PrettyTable(['Number', 'Activity'],
                        align='l')
    activities = ['Refuel', 'Buy products', 'Sale products', 'Buy components', 'List of planets']
    for n, activity in enumerate(activities):
        table.add_row([n + 1, activity])
    table.add_row(['0', 'Quit'])
    print(table)


EARTH = Planet('Earth')
context = {'ships': [StarShip('qwerty', 1000, EARTH, Engine(1, 20), Tank(100, 50)),
                     StarShip('Buran', 200, EARTH, Engine(2, 40), Tank(100, 50))],
           'planets': [Planet('Auropa'), EARTH, Planet('Qwerty')]}
EARTH.shop.components.append(Engine(2, 30))
EARTH.shop.components.append(Tank(200, 100))

if __name__ == '__main__':
    game_loop()
