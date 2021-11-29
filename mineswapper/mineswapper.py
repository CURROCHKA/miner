from random import shuffle


def correct_input(xy: list, field: list) -> bool:

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


def open_values(image: list) -> int:
    count_cell = 0

    for i in image:
        for j in i:
            if j != '#':
                count_cell += 1
    return count_cell


def calculate_value(field: list, x: int, y: int) -> int:
    mines = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < len(field) and 0 <= y + j < len(field[0]) and not (i == 0 and j == 0):
                if field[x + i][y + j] == 1:
                    mines += 1
    return mines


def new_image(field: list, image: list, x: int, y: int) -> list:

    new_value = calculate_value(field, x, y)
    image[x][y] = str(new_value)
    return image


def failed_image(field: list, image: list) -> list:

    for i, sublist in enumerate(field):
        for j, cell in enumerate(sublist):
            if cell == 1:
                image[i][j] = '*'
    return image


def show_image(image, field):
    for i in image:
        print(' '.join(i))
    print(field)


def make_move(field: list, image: list):
    x, y = int(input('Введите номер строки: ')), int(input('Введите номер столбца: '))
    xy = [x, y]
    if not correct_input(xy, field):
        return image, True

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


def generate_field(num_of_rows: int, num_of_columns: int, mines_number: int) -> list:
    image = [['#' for i in range(num_of_rows)] for j in range(num_of_columns)]
    field = [0] * (num_of_rows * num_of_columns - mines_number) + [1] * mines_number
    shuffle(field)
    l2 = []
    temp_list = []
    for i, j in enumerate(field):
        if not (i + 1) % num_of_columns:
            temp_list.append(j)
            l2.append(temp_list)
            temp_list = []
        else:
            temp_list.append(j)

    return l2, image


def is_finish():
    pass


def start_game():

    num_of_rows, num_of_columns = int(input('Введите кол-во строк: ')), int(input('Введите кол-во столбцов: '))
    mines_number = int(input('Введите количество мин: '))
    field, image = generate_field(num_of_rows, num_of_columns, mines_number)

    if mines_number == 0:
        failed_image(field, image)
        show_image(image, field)
        game_status = False
    else:
        game_status = True

    while game_status:
        if open_values(image) == num_of_rows * num_of_columns - mines_number:
            if num_of_rows == 1 and num_of_columns == 1:
                failed_image(field, image)
                break
            failed_image(field, image)
            game_status = False
        else:
            show_image(image, field)
            image, game_status = make_move(field, image)
    show_image(image, field)


def is_new_game() -> bool:
    pass


def main():
    #while is_new_game():
    start_game()


main()
