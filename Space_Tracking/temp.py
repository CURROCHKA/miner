import random


def create_boxes(n: int) -> dict:
    """Создание коробок с карточками внутри"""
    boxes = {}
    cards = list(range(1, n + 1))
    random.shuffle(cards)
    for i in range(n):
        boxes.update({i + 1: cards[i]})
    return boxes


def create_prisoners(n: int) -> dict:
    """Создание заключённых с кол-вом их попыток"""
    prisoners = {}
    for i in range(n):
        prisoners.update({i + 1: n // 2})
    return prisoners


def algorithm(prisoners: dict, boxes: dict) -> int:
    """Алгоритм прохода заключённых через комнату с коробками"""
    wins = 0
    lose = False
    for prisoner in prisoners:
        card = boxes[prisoner]
        prisoners[prisoner] -= 1
        while card != prisoner and prisoners[prisoner] > 0:
            card = boxes[card]
            prisoners[prisoner] -= 1
            if card != prisoner and prisoners[prisoner] == 0:
                lose = True
        if lose:
            break
        wins += 1
    return wins


def main():
    """Прогоняет алгоритм attempts раз с n заключёнными и коробками"""
    n = 100
    attempts = 100
    wins = 0
    for _ in range(attempts):
        boxes = create_boxes(n)
        prisoners = create_prisoners(n)
        if algorithm(prisoners, boxes) == n:
            wins += 1
    percentage_of_wins = wins * 100 / attempts
    percentage_of_loses = 100 - percentage_of_wins
    print(f'Процент побед: {percentage_of_wins}%\nПроцент поражений: {percentage_of_loses}%')


if __name__ == '__main__':
    main()
