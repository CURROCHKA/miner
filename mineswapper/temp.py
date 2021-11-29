from random import shuffle


def generate_field(num_of_rows: int, num_of_columns: int, mines_number: int) -> list:
    image = [['#' for i in range(num_of_rows)] for j in range(num_of_columns)]
    field = [0] * (num_of_rows * num_of_columns - mines_number) + [1] * mines_number
    field_test = [[0 for i in range(num_of_rows)] for j in range(num_of_columns)]
    return field


print(generate_field(2, 2, 2))
