from itertools import chain
from typing import Iterable

l = chain([1, 3, [2, 3, 4], 2, 5, 0], (1, 2, (14115, 15230), 1, 13131))
for i in l:
    print(i)
print()


def my_chain_flatten(*iterables):
    for i in iterables:
        for j in i:
            if isinstance(j, Iterable):
                yield from my_chain_flatten(j)
            else:
                yield j


def my_chain(*iterables):
    for i in iterables:
        for j in i:
            yield j


def chain_file(file_txt):
    with open(file_txt) as f:

        for i in f:
            yield i.strip()


l = my_chain([1, 3, [2, 3, 4], 2, 5, 0], (1, 2, (14115, 15230), 1, 13131))
for i in l:
    print(i)
print()

l = my_chain_flatten([1, 3, [2, 3, 4], 2, 5, 0], (1, 2, (14115, (888888888, 1111111), 15230), 1, 13131))
for i in l:
    print(i)


# COLORS = ['GREEN', 'ORANGE', 'BLUE', 'RED', 'YELLOW', 'WHITE']
# qube = []
# rotate_x = True
# rotate_y = False
# count = 0
# n = 2
# for i in range(6):
#     qube.append([[COLORS[i]] * 3] * 3)
#
# while count != n:
#     if rotate_x:
#         qube[3][:2], qube[2][:2], qube[1][:2], qube[0][:2] = qube[0][:2], qube[3][:2], qube[2][:2], qube[1][:2]
#         qube[4][0][0], qube[4][0][1], qube[4][0][2], \
#         qube[4][1][2], qube[4][2][2], \
#         qube[4][2][1], qube[4][2][2] = qube[4][2][0], qube[4][1][0], qube[4][0][0], \
#                                        qube[4][0][1], qube[4][0][2], \
#                                        qube[4][1][2], qube[4][2][0]
#         count += 1
#         rotate_x = False
#         rotate_y = True
#     elif rotate_y:
#         list1 = qube
#         list1[4][0][1] = 'BLUE'
#         print(list1)
#         qube[4][0][1] = 'BLUE'
#         # qube[3][2][2], qube[3][1][2], qube[3][0][2], \
#         # qube[3][0][1], qube[3][0][0], \
#         # qube[3][1][0], qube[3][2][0], \
#         # qube[3][2][1], qube[3][2][0] = qube[3][2][0], qube[3][2][1], qube[3][2][2], \
#         #                                qube[3][1][2], qube[3][0][2], \
#         #                                qube[3][0][1], qube[3][0][0], \
#         #                                qube[3][1][0], qube[3][2][2]
#         count += 1
#         rotate_y = False
#         rotate_x = True
#
# print(qube)
