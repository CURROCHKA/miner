def generate_field(num_of_rows: int, num_of_columns: int, mines_number: int) -> list:

    from random import randint
    from random import shuffle
    field = [0] * (num_of_rows * num_of_columns)
    print(shuffle(field))
    #field = [[randint(0, 1) for i in range(num_of_rows)] for j in range(num_of_columns)]
    image = [['#' for i in range(num_of_rows)] for j in range(num_of_columns)]

    return field, image


print(generate_field(3, 3, 1))
