def failed_image(field, image):
    pass


def is_mine(field, x, y) -> bool:
    pass


def open_values(image) -> int:
    pass


def calculate_value(image, x, y):
    mines = 0
    #for
        #for
    return mines


def new_image(image, x, y):
    new_value = calculate_value(image, x, y)
    image[x][y] = new_value
    return image


def show_image(image):
    pass


def make_move(field, image):
    x, y = input(), input()
    #is correct input
    #if not
        #return image, True

    #is clicked ???
    #if yes
        #return image, True

    #if is_mine(field, x, y):
        #yes
        #image = failed_image(field, image)
        #return image, False

        #not
        #image = new_image(image, x, y)
        #return image, True


def generate_field(n, m, mines_number) -> tuple:
    pass
    #return field, image


def is_finish():
    pass


def start_game():

    n, m, mines_number = input(), input(), input()
    field, image = generate_field(n, m, mines_number)
    game_status = True

    while game_status:
        if open_values(image) == n * m - mines_number:
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image)


def is_new_game() -> bool:
    pass


def main():
    while is_new_game():
        start_game()


main()
