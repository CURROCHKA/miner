from random import shuffle


def correct_field(num_of_rows, num_of_columns, mines_number) -> bool:

    if all(i.isdigit() for i in [num_of_rows, num_of_columns, mines_number]):
        if int(num_of_rows) > 0 and int(num_of_columns) > 0 and int(mines_number) > 0:
            return True
    print('Пожалуйста, введите верные данные')
    return False


def correct_input(x: str, y: str, field: list) -> bool:

    if len([x, y]) == 2:
        if all(i.isdigit() for i in [x, y]) \
                and all(int(i) >= 0 for i in [x, y]) \
                and int(x) <= len(field[0]) - 1 and int(y) <= len(field) - 1:
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


def show_image(image):
    for i in image:
        print(' '.join(i))


def make_move(field: list, image: list):
    x, y = input('Введите номер строки: '), input('Введите номер столбца: ')
    if not correct_input(x, y, field):
        return image, True

    # is clicked ???
    # if yes
        # return image, True
    x = int(x)
    y = int(y)
    if is_mine(field, x, y):
        print('Game over!')
        image = failed_image(field, image)
        show_image(image)
        return image, False
    else:
        image = new_image(field, image, x, y)
        return image, True


def generate_field(num_of_rows: str, num_of_columns: str, mines_number: str) -> list:
    present_field = []
    temp_list = []
    image = [['#' for i in range(int(num_of_rows))] for j in range(int(num_of_columns))]
    field = [0] * (int(num_of_rows) * int(num_of_columns) - int(mines_number)) + [1] * int(mines_number)
    shuffle(field)
    for i, j in enumerate(field):
        if not (i + 1) % int(num_of_columns):
            temp_list.append(j)
            present_field.append(temp_list)
            temp_list = []
        else:
            temp_list.append(j)

    return present_field, image


def is_finish():
    pass


def start_game():
    field_status = True

    while field_status:

        print('Выберите уровень сложонсти: easy, medium, hard, custom')
        difficult = difficult_lvl()

        if difficult == 'custom':
            num_of_rows, num_of_columns = input('Введите кол-во строк: '), input('Введите кол-во столбцов: ')
            mines_number = input('Введите кол-во мин: ')
            if correct_field(num_of_rows, num_of_columns, mines_number):
                field, image = generate_field(num_of_rows, num_of_columns, mines_number)
                field_status = False
        else:
            num_of_rows, num_of_columns, mines_number = difficult
            field, image = generate_field(num_of_rows, num_of_columns, mines_number)
            field_status = False

    game_status = True

    while game_status:
        if open_values(image) == int(num_of_rows) * int(num_of_columns) - int(mines_number):
            print('Победа!')
            failed_image(field, image)
            show_image(image)
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image)


def difficult_lvl():
    easy = (3, 3, 3)
    medium = (5, 5, 7)
    hard = (7, 7, 18)
    difficult_status = True
    while difficult_status:
        difficult = input()
        if difficult == 'easy':
            difficult_status = False
            return easy
        elif difficult == 'medium':
            difficult_status = False
            return medium
        elif difficult == 'hard':
            difficult_status = False
            return hard
        elif difficult == 'custom':
            difficult_status = False
            return 'custom'
        else:
            print('Выберите уровень сложонсти: easy, medium, hard, custom')


def is_new_game() -> bool:
    new_game_status = True
    while new_game_status:
        print('Новая игра: Y', 'Завершить игру: N', sep='\n')
        string = input()
        if string == 'Y':
            new_game_status = False
            return True
        elif string == 'N':
            new_game_status = False
            return False


def main():
    while is_new_game():
        start_game()


main()
