from planet import Planet
from star_ship import StarShip, Engine, Tank
from prettytable import PrettyTable
from time import sleep
import re


def game_loop():
    while True:
        print_ships()
        print('Enter the "Next" ot "Next # (the number of moves you want to skip)" command to skip the move')
        ship = input('Enter the name of the ship you want to interact with (or quit the game - 0): ')
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


def identify_ship(ship_name: str) -> StarShip:
    for ship in context['ships']:
        if ship_name.lower() == ship.name.lower() and ship.inactivity_moves == 0:
            return ship


def ship_activities(ship: StarShip):
    flag = True
    while True:
        if not flag:
            break
        print_table_activities()
        try:
            player_input = int(input('Choose activity (Number): '))
            if player_input == 0:
                break
        except ValueError:
            print('\nEnter a positive integer\n')
            flag = False
            ship_activities(ship)

        if not player_input > 0:
            print('\nEnter a positive integer\n')
            sleep(2)
            continue
        elif player_input == 1:
            first_activity(ship)
        elif player_input == 2:
            second_activity(ship)
        elif player_input == 3:
            third_activity(ship)
        # elif player_input == 4:
        #     fourth_activity(ship)
        elif player_input == 5:
            if fifth_activity(ship):
                break


def first_activity(ship: StarShip):
    while True:
        try:
            fuel = int(input('Enter the units of fuel you want (or choose another activity - 0): '))
            if fuel == 0:
                break
        except ValueError:
            first_activity(ship)
        ship.make_refuel(fuel)
        sleep(2)


def second_activity(ship: StarShip):
    flag = True
    while True:
        if not flag:
            break
        print_products(ship)
        product = input('Enter the name of the product you want to buy (or choose another activity - 0): ')
        if product == '0':
            break
        try:
            amount = int(input('Enter the amount of the product you want to buy (or choose another activity - 0): '))
            if amount == 0:
                break
        except ValueError:
            print('\nEnter a positive integer\n')
            sleep(1)
            flag = False
            second_activity(ship)

        products = ship.location.stock.products
        if product in products and amount != 0:
            ship.make_buy(product, amount)
            sleep(2)
            flag = False
            second_activity(ship)
        else:
            print('There is no such product in the list')


def third_activity(ship: StarShip):
    flag = True
    while True:
        if not flag:
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

        cargo = ship.cargo_bay.cargo
        if product in cargo and amount != 0:
            ship.make_sale(product, amount)
            sleep(2)
            flag = False
            third_activity(ship)
        else:
            print('There is no such product in the list')


def fourth_activity(ship: StarShip):
    flag = True
    while True:
        if not flag:
            break
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


def fifth_activity(ship: StarShip):
    planet = ''
    while planet != '0':
        print_planets(ship)
        planet = input('Enter the name of the planet you want to go to (or choose another activity - 0): ')
        if move_to_planet(planet, ship):
            return True
    return False


def move_to_planet(target_planet_name: str, ship: StarShip):
    target_planet_name = target_planet_name.lower()
    for planet in context['planets']:
        if target_planet_name == planet.name.lower():
            ship.move_to_planet(planet)
            sleep(2)
            break
    return target_planet_name == ship.location.name.lower()


def print_products(ship: StarShip):
    planet = ship.location
    table = PrettyTable(['Product', 'Stock Amount', 'Your amount', 'Price'], title='Products', align='l', padding_width=2)
    for product in planet.stock.products:
        if product != 'fuel':
            stock_amount, price = planet.stock.products[product]
            ship_amount = ship.cargo_bay.cargo[product]
            table.add_row([product.title(), stock_amount, ship_amount, price])
    print(table)


def print_components(ship: StarShip):
    planet = ship.location
    table = PrettyTable(['Number', 'Component', 'Parameters', 'Price'], title='Components', align='l')
    for n, component in enumerate(planet.shop.components):
        component_name = component.__class__.__name__
        parameter = f'Speed {component.speed}' if component_name == 'Engine' else f'Volume {component.capacity}'
        price = component.price
        table.add_row([n + 1, component_name, parameter, price])
    print(table)


def print_planets(ship: StarShip):
    table = PrettyTable(['Planet', 'Distance'], title='Planets', align='l')
    for planet in context['planets']:
        if planet.name != ship.location.name:
            distance = ship.ship_system.NavigationModule.get_distance(ship.location, planet)
            table.add_row([planet.name, distance])
    print(table)


def print_ships():
    table = PrettyTable(['Ship', 'Status'], align='l')
    for ship in context['ships']:
        status = f'{ship.inactivity_moves} moves remaining for "Active"' if ship.inactivity_moves > 0 else 'Active'
        table.add_row([ship.name, status])
    print(table)


def print_table_activities():
    table = PrettyTable(['Activity', 'Number'], align='l')
    activities = ['Refuel', 'Buy products', 'Sale products', 'Buy components', 'Move to another planet']
    for i, activity in enumerate(activities):
        table.add_row([activity, i + 1])
    table.add_row(['Quit', '0'])
    print(table)


EARTH = Planet('Earth')
context = {'ships': [StarShip('qwerty', 1000, EARTH, Engine(1, 20), Tank(100, 50)), StarShip('Buran', 200, EARTH, Engine(2, 40), Tank(100, 50))],
           'planets': [Planet('Auropa'), EARTH, Planet('Qwerty')]}
EARTH.shop.components.append(Engine(2, 30))
EARTH.shop.components.append(Tank(200, 100))

game_loop()
