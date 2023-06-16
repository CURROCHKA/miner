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
    except ValueError:
        print('\nEnter a positive integer\n')
        return None
    ship = context['ships'][number_ship - 1]
    if ship.inactivity_moves == 0:
        return ship


def ship_activities(ship: StarShip):
    flag = True
    while True:
        if not flag:
            break
        print_table_activities()

        flag, player_input = correct_int_input('Choose activity (Number): ')
        if not flag:
            ship_activities(ship)
            break
        elif player_input == 0:
            break

        elif player_input == 1:
            first_activity(ship)
        elif player_input == 2:
            second_activity(ship)
        elif player_input == 3:
            third_activity(ship)
        elif player_input == 4:
            fourth_activity(ship)
        elif player_input == 5:
            if fifth_activity(ship):
                break


def correct_int_input(msg: str) -> Union[Tuple[bool, int], Tuple[bool, None]]:
    try:
        inp = int(input(msg))
    except ValueError:
        print('Enter a positive integer')
        return False, None
    if inp >= 0:
        return True, inp
    return False, None


def first_activity(ship: StarShip):
    while True:
        flag, fuel = correct_int_input('Enter the units of fuel you want (or choose another activity - 0): ')
        if not flag:
            first_activity(ship)
            break
        elif fuel == 0:
            break
        ship.make_refuel(fuel)
        sleep(2)


def second_activity(ship: StarShip):
    stock_products = ship.location.stock.products
    products = {}
    for i, p in enumerate(stock_products):
        products.update({i + 1: p})
    while True:
        print_products(ship, products)

        flag, num_product = correct_int_input('Enter a number of the product you want to buy (or choose another '
                                              'activity - 0): ')
        if not flag:
            second_activity(ship)
            break
        elif num_product == 0:
            break

        flag, amount = correct_int_input('Enter the amount of the product you want to buy (or choose another activity '
                                         '- 0): ')
        if not flag:
            second_activity(ship)
            break
        elif amount == 0:
            break

        if num_product in products.keys() and amount != 0:
            ship.make_buy(products[num_product], amount)
            sleep(2)
            second_activity(ship)
            break
        else:
            print('There is no such product in the list')


def third_activity(ship: StarShip):
    stock_products = ship.location.stock.products
    products = {}
    for i, p in enumerate(stock_products):
        products.update({i + 1: p})
    while True:
        print_products(ship, products)

        flag, num_product = correct_int_input(
            'Enter a number of the product you want to sale (or choose another activity - 0): ')
        if not flag:
<<<<<<< Updated upstream
            break
        print_products(ship)
        product = input('Enter the name of the product you want to sale (or choose another activity - 0): ')
        if product == '0':
            break
        try:
            amount = int(input('Enter the amount of the product you want to sale (or choose another activity - 0): '))
            if amount == 0:
                break
            elif amount < 0:
                print('\nEnter a positive integer\n')
                sleep(1)
                flag = False
                third_activity(ship)
                break
        except ValueError:
            print('\nEnter a positive integer\n')
            sleep(1)
            flag = False
            third_activity(ship)
            break
=======
            third_activity(ship)
            break
        elif num_product == 0:
            break
        flag, amount = correct_int_input('Enter the amount of the product you want to sale (or choose another '
                                         'activity - 0): ')
        if not flag:
            third_activity(ship)
            break
>>>>>>> Stashed changes

        cargo = ship.cargo_bay.cargo
        product = products[num_product]
        if product in cargo and amount != 0:
            ship.make_sale(product, amount)
            sleep(2)
            third_activity(ship)
            break
        else:
            print('There is no such product in the list')


def fourth_activity(ship: StarShip):
    shop_components = ship.location.shop.components
    components = {}
    for i, c in enumerate(shop_components):
        components.update({i + 1: c})
    while True:
        print_components(ship, components)

        flag, num_component = correct_int_input('Enter a number of the component you want to buy (or choose another '
                                                'activity - 0): ')
        if not flag:
            fourth_activity(ship)
            break
        elif num_component == 0:
            break

        component = components[num_component]
        if component in shop_components:
            ship.buy_new_component(component)
            sleep(2)
            fourth_activity(ship)
            break
<<<<<<< Updated upstream
        print_components(ship)
        try:
            number = int(input('Enter the number of the component you want to buy (or choose another activity - 0): '))
            if number == 0:
                break
        except ValueError:
            print('\nEnter a positive integer\n')
            sleep(1)
            flag = False
            fourth_activity(ship)
        ...
=======
>>>>>>> Stashed changes


def fifth_activity(ship: StarShip):
    planets = {}
    for i, planet in enumerate(context['planets']):
        planets.update({i + 1: planet})

    while True:
        print_planets(ship)
        flag, num_planet = correct_int_input('Enter a number of the planet you want to go to (or choose another '
                                             'activity - 0): ')
        if not flag:
            first_activity(ship)
            break
        elif num_planet == 0:
            break

        planet = planets[num_planet] if planets[num_planet] is not ship.location else planets[num_planet + 1]
        ship.move_to_planet(planet)
        return True
    return False


def print_products(ship: StarShip, name_products: dict):
    table = PrettyTable(['Number', 'Product', 'Stock Amount', 'Your amount', 'Price'],
                        title='Products',
                        align='l',
                        padding_width=2)
    stock_products = ship.location.stock.products
    for num_product in name_products:
        if name_products[num_product] != 'fuel':
            product = name_products[num_product]
            stock_amount, price = stock_products[product]
            ship_amount = ship.cargo_bay.cargo[product]
            table.add_row([num_product, product.title(), stock_amount, ship_amount, price])
    print(table)


<<<<<<< Updated upstream
def print_components(ship: StarShip):
    planet = ship.location
    table = PrettyTable(['Number', 'Component', 'Parameters', 'Price'], title='Components', align='l')
    for n, component in enumerate(planet.shop.components):
=======
def print_components(ship: StarShip, components: dict):
    table = PrettyTable(['Number', 'Component', 'Parameters', 'Parameters of your ship', 'Price'],
                        title='Components',
                        align='l')
    for num_component in components:
        component = components[num_component]
>>>>>>> Stashed changes
        component_name = component.__class__.__name__
        ship_parameter = f'Speed {ship.engine.speed}' if component_name == 'Engine' else f'Volume {ship.tank.capacity}'
        parameter = f'Speed {component.speed}' if component_name == 'Engine' else f'Volume {component.capacity}'
        price = component.price
<<<<<<< Updated upstream
        table.add_row([n + 1, component_name, parameter, price])
=======
        table.add_row([num_component, component_name, parameter, ship_parameter, price])
>>>>>>> Stashed changes
    print(table)


def print_planets(ship: StarShip):
    table = PrettyTable(['Number', 'Planet', 'Distance'],
                        title='Planets',
                        align='l')
    num = -1
    for i, planet in enumerate(context['planets']):
        if planet is not ship.location:
            distance = ship.ship_system.NavigationModule.get_distance(ship.location, planet)
            table.add_row([i + 1 if num == -1 else i, planet.name, distance])
        else:
            num = i
    print(table)


def print_ships():
    table = PrettyTable(['Number', 'Ship', 'Status'],
                        align='l')
    for i, ship in enumerate(context['ships']):
        status = f'{ship.inactivity_moves} moves remaining for "Active"' if ship.inactivity_moves > 0 else 'Active'
        table.add_row([i + 1, ship.name, status])
    print(table)


def print_table_activities():
    table = PrettyTable(['Number', 'Activity'],
                        align='l')
    activities = ['Refuel', 'Buy products', 'Sale products', 'Buy components', 'Move to another planet']
    for i, activity in enumerate(activities):
        table.add_row([i + 1, activity])
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
