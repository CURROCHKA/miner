"""

field = [[1, 0, 0], [1, 1, 0], [0, 0, 1]]
image = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

"""

"""
(i, j)

(i-1, j)
(i+1, j)
(i, j-1)
(i, j+1)
(i+1, j+1)
(i-1, j-1)
(i+1, j-1)
(i-1, j+1)
"""
image = [['#', '3', '#'],
         ['2', '#', '#'],
         ['#', '#', '1']]


def show_image(image):
    for i in image:
        print(' '.join(i))


show_image(image)


def open_values(image: list) -> int:
    count = 0

    for i in image:
        for j in i:
            if j != '#':
                count += 1
    return count


print(open_values(image))


def generate_field(num_of_rows: int, num_of_columns: int, mines_number: int) -> list:
    from random import randint
    field = [[]]

    return field #, image


print(generate_field(3,3,1))