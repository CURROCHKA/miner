from time import sleep

def check_square(
    start_pointer: tuple,
    matrix: list,
) -> bool:
    """
    Recursively change pointer, check the square's type and change the color of the square.
    :param start_pointer:
    :param matrix:
    :param grid_display:
    :param square_params:
    :return:
    """
    #sleep(0.01)
    x, y = start_pointer[0], start_pointer[1]

    if matrix[x][y] == 1:
        print('wall on', x, y)
        return False
    elif matrix[x][y] == 3:
        print('already visited', x, y)
        return False
    elif x == len(matrix) - 1 and y == len(matrix[0]) - 1:
        print('win on', x, y)
        return True
    print('visiting', x, y)
    matrix[x][y] = 3

    if (
        (x < len(matrix) - 1 and check_square((x + 1, y), matrix))
        or (y > 0 and check_square((x, y - 1), matrix))
        or (x > 0 and check_square((x - 1, y), matrix))
        or (y < len(matrix[0]) - 1 and check_square((x, y + 1), matrix))
    ):
        return True
    return False


matrix = [[0, 0, 1, 0],
          [1, 0, 1, 1],
          [0, 0, 1, 1],
          [0, 0, 0, 0]]

print(check_square((0, 0), matrix))
