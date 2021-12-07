'''if mines_number == 0:
    failed_image(field, image)
    show_image(image)
    game_status = False
else:
    game_status = True'''


def correct_field(num_of_rows, num_of_columns, mines_number) -> bool:
    if all(i.isdigit() for i in [num_of_rows, num_of_columns, mines_number]):
        if int(num_of_rows) > 0 and int(num_of_columns) > 0 and int(mines_number) > 0:
            return True
    return False


print(correct_field(input(), input(), input()))
