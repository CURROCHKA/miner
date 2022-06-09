from star_ship import *
from planet import *


class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 2000000

    def buy_ship(self, ship, planet):
        pass


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
