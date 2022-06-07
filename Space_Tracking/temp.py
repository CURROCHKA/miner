'''def __count_freespace(self) -> int:
    count = 0
    for i in range(ROWS):
        for j in range(COLUMNS):
            if not self.__check_planets(i, j):
                count += 1
    return count


def __check_planets(self, x: int, y: int) -> bool:
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < ROWS and 0 <= y + j < COLUMNS and not (i == 0 and j == 0) \
                    and [x + i, y + j] in planets_coord:
                return True
    return False

'''


def correct_number(number):
    count = 0
    if type(number) is str or type(number) is int:
        number = str(number)
        count += 1
    if count == 1 and number.isdigit():
        count += 1
    if count == 1:
        for i in range(len(number) - len([i for i in number if not i.isdigit()])):
            if not number[i].isdigit():
                print('1')
                number = number.replace(number[i], '')
        count += 1
        print(number)
    if count == 2 and len(number) == 11 or len(number) == 10:
        count += 1
    if count == 3 and number[0] == '9':
        return '+7' + ' ' + number[0:3] + '-' + number[3:6] + '-' + number[6:8] + '-' + number[8:10]
    if count == 3 and number[0] == '7':
        return '+' + number[0] + ' ' + number[1:4] + '-' + number[4:7] + '-' + number[7:9] + '-' + number[9:11]
    if count == 3 and number[0] == '8':
        return '+7' + ' ' + number[1:4] + '-' + number[4:7] + '-' + number[7:9] + '-' + number[9:11]


print(correct_number('+79157420013%@%&*^!(^!)%(^!'))

