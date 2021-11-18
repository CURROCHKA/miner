from time import sleep

from maze_solver import can_exit

matrix1 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

matrix2 = [
    [0, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0],
]

matrix3 = [
    [0, 0, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0],
]

matrix4 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


matrix5 = [
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

matrix6 = [
    [0, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 1],
    [1, 1, 0, 0, 1, 1, 1],
]

matrix7 = [
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
]


matrix8 = [
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0],
]


matrix9 = [[0]]


matrix10 = [[1]]

matrix11 = [[]]


matrix12 = [[0, 0, 0], [0, 2, 0], [0, 0, 0]]

matrix13 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def test1():
    assert can_exit(matrix1) is True
    sleep(1)


def test2():
    assert can_exit(matrix2) is True
    sleep(1)


def test3():
    assert can_exit(matrix3) is True
    sleep(1)


def test4():
    assert can_exit(matrix4) is True
    sleep(1)


def test5():
    assert can_exit(matrix5) is True
    sleep(1)


def test6():
    assert can_exit(matrix6) is False
    sleep(1)


def test7():
    assert can_exit(matrix7) is False
    sleep(1)


def test8():
    assert can_exit(matrix8) is True
    sleep(1)


def test9():
    assert can_exit(matrix9) is True
    sleep(1)


def test10():
    assert can_exit(matrix10) is False
    sleep(1)


def test11():
    assert can_exit(matrix11) is False
    sleep(1)


def test12():
    assert can_exit(matrix12) is False
    sleep(1)


def test13():
    assert can_exit(matrix13) is True
    sleep(1)
