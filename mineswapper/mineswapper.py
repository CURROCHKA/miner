def correct_input(xy, field) -> bool:

    if len(xy) == 2 \
            and all(isinstance(i, int) for i in xy) \
            and all(i >= 0 for i in xy) \
            and xy[0] <= len(field[0]) - 1 and xy[1] <= len(field) - 1:
        return True
    print('Пожалуйста, введите верные координаты')
    return False


def is_mine(field: list, x: int, y: int) -> bool:

    if field[x][y] == 1:
        return True
    return False


def open_values(image) -> int:
    pass


def calculate_value(field, x, y) -> int:

    mines = 0
    return mines


def new_image(field, image, x, y) -> list:

    new_value = calculate_value(field, x, y)
    image[x][y] = new_value
    return image


def failed_image(field, image) -> list:

    for i in range(len(field)):
        for j in range(len(image)):
            if 1 == field[i][j]:
                image[i][j] = '*'
    return image


def show_image(image):
    pass


def make_move(field, image):

    x, y = int(input()), int(input())
    xy = [x, y]
    if correct_input(xy, field):
        return image, False

    # is clicked ???
    # if yes
        # return image, True

    if is_mine(field, x, y):
        print('Game over')
        image = failed_image(field, image)
        return image, False
    else:
        image = new_image(field, image, x, y)
        return image, True


def generate_field(num_of_rows, num_of_columns, mines_number) -> tuple:
    pass
    # return field, image


def is_finish():
    pass


def start_game():

    num_of_rows, num_of_columns = map(int, input('Введите количество строк и столбцов: ').split())
    mines_number = int(input('Введите количество мин: '))
    field, image = generate_field(num_of_rows, num_of_columns, mines_number)
    game_status = True

    while game_status:
        if open_values(image) == num_of_rows * num_of_columns - mines_number: #win
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image)


def is_new_game() -> bool:
    pass


def main():

    while is_new_game():
        start_game()


#main()

