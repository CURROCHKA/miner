def correct_input(xy, field):
    if len(xy) > 2 or len(xy) < 2:
        return 'Пожалуйста, введите верные координаты'
    elif not xy[0].isdigit() or not xy[1].isdigit():
        return 'Пожалуйста, введите верные координаты'
    elif xy[0] < 0 or xy[1] < 0:
        return 'Пожалуйста, введите верные координаты'
    elif xy[0] > len(field[0]) or xy[1] > len(field):
        return 'Пожалуйста, введите верные координаты'
    return True

def failed_image(field, image):
    pass


def is_mine(field, x, y) -> bool:
    pass


def open_values(image) -> int:
    pass


def calculate_value(image, x, y):
    mines = 0
    # for
        # for
    return mines


def new_image(image, x, y):
    new_value = calculate_value(image, x, y)
    image[x][y] = new_value
    return image


def show_image(image):
    pass


def make_move(field, image):
    x, y = int(input()), int(input())
    xy = [x, y]
    if correct_input(xy, field):
        return False

    # is clicked ???
    # if yes
        # return image, True

    # if is_mine(field, x, y):
        # yes
        # image = failed_image(field, image)
        # return image, False

        # not
        # image = new_image(image, x, y)
        # return image, True


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
        if open_values(image) == num_of_rows * num_of_columns - mines_number:
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image) # game_status


def is_new_game() -> bool:
    pass


def main():
    while is_new_game():
        start_game()


main()
