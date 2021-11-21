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
        print(str(i)[1:-1])


# print(show_image(image))


def open_values(image: list) -> int:
    count = 0

    for i in image:
        for j in i:
            if j != '#':
                count += 1
    return count


print(open_values(image))