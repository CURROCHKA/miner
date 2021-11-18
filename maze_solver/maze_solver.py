"""

"""

from time import sleep

import pygame


def check_correct(matrix: list) -> bool:
    """
    Check if input matrix is correct
    :param field: input field
    :return:
    """
    if (
        len(matrix)
        and isinstance(matrix, list)
        and all(len(matrix[i]) for i, _ in enumerate(matrix))
        and all(len(matrix[i]) == len(matrix[0]) for i, _ in enumerate(matrix))
        and all(i in (1, 0) for i in [j for sublist in matrix for j in sublist])
        and all(isinstance(i, list) for i in matrix)
    ):
        return True
    return False


def create_square(
    x: int, y: int, color: tuple, grid_display: pygame.Surface, square_params: tuple
) -> None:
    """
    Draw the square on the gird.
    :param x:
    :param y:
    :param color:
    :param grid_display: pygame object for representing images
    :param square_params: size of the square
    :return:
    """
    pygame.draw.rect(grid_display, color, [x, y, square_params[0], square_params[1]])


def generate_maze(
    grid_display: pygame.Surface, matrix: list, square_params: tuple
) -> None:
    """
    Draw walls and background on the gird
    :param grid_display:
    :param matrix:
    :param square_params:
    :return:
    """
    pointer_y = 0
    for row in matrix:
        pointer_x = 0
        for item in row:
            if item == 0:
                create_square(
                    pointer_x, pointer_y, (255, 255, 255), grid_display, square_params
                )
            else:
                create_square(
                    pointer_x, pointer_y, (0, 0, 0), grid_display, square_params
                )

            pointer_x += square_params[0]
        pointer_y += square_params[1]

    pygame.display.update()


def check_square(
    start_pointer: tuple,
    matrix: list,
    grid_display: pygame.Surface,
    square_params: tuple,
) -> bool:
    """
    Recursively change pointer, check the square's type and change the color of the square.
    :param start_pointer:
    :param matrix:
    :param grid_display:
    :param square_params:
    :return:
    """
    sleep(0.04)
    x, y = start_pointer[0], start_pointer[1]

    if matrix[x][y] == 1 or matrix[x][y] == 3:
        return False
    elif x == len(matrix) - 1 and y == len(matrix[0]) - 1:
        create_square(
            y * square_params[1],
            x * square_params[0],
            (0, 255, 0),
            grid_display,
            square_params,
        )
        pygame.display.update()
        return True

    create_square(
        y * square_params[1],
        x * square_params[0],
        (0, 0, 255),
        grid_display,
        square_params,
    )
    pygame.display.update()

    matrix[x][y] = 3
    create_square(
        y * square_params[1],
        x * square_params[0],
        (255, 125, 125),
        grid_display,
        square_params,
    )

    if (
        (
            x < len(matrix) - 1
            and check_square((x + 1, y), matrix, grid_display, square_params)
        )
        or (y > 0 and check_square((x, y - 1), matrix, grid_display, square_params))
        or (x > 0 and check_square((x - 1, y), matrix, grid_display, square_params))
        or (
            y < len(matrix[0]) - 1
            and check_square((x, y + 1), matrix, grid_display, square_params)
        )
    ):
        return True
    return False


def generate_grid(rows: int, columns: int, square_params: tuple) -> pygame.Surface:
    """
    Generate the game grid
    :param rows:
    :param columns:
    :param square_params:
    :return:
    """
    return pygame.display.set_mode(
        (columns * square_params[1], rows * square_params[0])
    )


def can_exit(matrix: list) -> bool:
    """
    Check if the maze is passable
    :param matrix: Maze represented as 2d matrix
    :return:
    """
    square_params = (50, 50)
    start_pointer = (0, 0)
    rows = len(matrix)
    columns = len(matrix[0])

    if not check_correct(matrix):
        return False

    grid_display = generate_grid(rows, columns, square_params)

    generate_maze(grid_display, matrix, square_params)

    if check_square(start_pointer, matrix, grid_display, square_params):

        return True
    return False


if __name__ == "__main__":
    matrix = [
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    can_exit(matrix)
    sleep(3)
