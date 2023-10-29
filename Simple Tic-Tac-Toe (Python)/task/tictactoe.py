
SYMBOL_X = "X"
SYMBOL_O = "O"
SYMBOL_EMPTY = "_"
current_symbol = SYMBOL_X


def print_line():
    print("-" * 9)


def print_formatted_row(symbols):
    print(f'| {" ".join(symbols).replace("_", " ")} |')


def make_list_of_rows_from_str(s: str) -> list:
    return [list(s[i:i+3]) for i in range(0, len(s), 3)]


def print_field(field: list):
    print_line()
    for row in field:
        print_formatted_row(row)
    print_line()


def is_only_one_unique_symbol(l: list) -> bool:
    return len(set(l)) == 1


def calc_quantity_of_win_situations(lst: list) -> dict:
    result = {SYMBOL_X: 0, SYMBOL_O: 0, SYMBOL_EMPTY: 0}

    if type(lst[0]) is list:
        for sublist in lst:
            if is_only_one_unique_symbol(sublist):
                result[sublist[0]] += 1
    else:
        if is_only_one_unique_symbol(lst):
            result[lst[0]] += 1

    return result


def analyze_field(field: list) -> str:
    STATE_IMPOSSIBLE = "Impossible"
    STATE_DRAW = "Draw"
    STATE_X_WINS = "X wins"
    STATE_O_WINS = "O wins"

    symbol_counter = {SYMBOL_X: 0, SYMBOL_O: 0, SYMBOL_EMPTY: 0}

    max_col = len(field[0])
    max_row = len(field)
    cols = [[] for _ in range(max_col)]
    rows = [[] for _ in range(max_row)]
    fdiag = []
    bdiag = []

    # It can be that X or Y fill several lines at once. For example: XXXXOOXOO
    win_counter = {SYMBOL_X: 0, SYMBOL_O: 0}

    for x in range(max_col):
        for y in range(max_row):
            current_symbol = field[y][x]

            symbol_counter[current_symbol] += 1

            # Fill collections of rows, cols, and diagonals
            cols[x].append(current_symbol)
            rows[y].append(current_symbol)
            if x == y:
                fdiag.append(current_symbol)
            if x + y == max_col - 1:
                bdiag.append(current_symbol)

    # Let's calc how many win situations has X or O
    cols_win_counter = calc_quantity_of_win_situations(cols)
    rows_win_counter = calc_quantity_of_win_situations(rows)
    fdiag_win_counter = calc_quantity_of_win_situations(fdiag)
    bdiag_win_counter = calc_quantity_of_win_situations(bdiag)
    for key in [SYMBOL_X, SYMBOL_O]:
        win_counter[key] += cols_win_counter[key]
        win_counter[key] += rows_win_counter[key]
        win_counter[key] += fdiag_win_counter[key]
        win_counter[key] += bdiag_win_counter[key]

    # Impossible: There are a lot more X's than O's or vice versa (the difference should be 1 or 0;
    # if the difference is 2 or more, then the game state is impossible).
    if (abs(symbol_counter[SYMBOL_O] - symbol_counter[SYMBOL_X]) >= 2
            or win_counter[SYMBOL_X] > 1
            or win_counter[SYMBOL_O] > 1
            or win_counter[SYMBOL_X] and win_counter[SYMBOL_O]):
        return STATE_IMPOSSIBLE
    elif win_counter[SYMBOL_X]:
        return STATE_X_WINS
    elif win_counter[SYMBOL_O]:
        return STATE_O_WINS
    elif not symbol_counter[SYMBOL_EMPTY]:
        return STATE_DRAW


def check_user_input(user_input: list, game_field):
    if len(user_input) != 2:
        return "User entered wrong number of parameters!"

    try:
        user_coordinates = [int(user_string) for user_string in user_input]
    except ValueError:
        return "You should enter numbers!"

    for i in range(len(user_coordinates)):
        if not 0 < user_coordinates[i] < 4:
            return "Coordinates should be from 1 to 3!"

    if game_field[user_coordinates[0] - 1][user_coordinates[1] - 1] != SYMBOL_EMPTY:
        return "This cell is occupied!"


def change_game_field(user_input: list, game_field):
    global current_symbol
    game_field[int(user_input[0]) - 1][int(user_input[1]) - 1] = current_symbol
    current_symbol = SYMBOL_X if current_symbol == SYMBOL_O else SYMBOL_O


game_code = "_" * 9
field = make_list_of_rows_from_str(game_code)
print_field(field)

while True:
    user_move = input().split()

    user_input_check_result = check_user_input(user_move, field)
    if user_input_check_result:
        print(user_input_check_result)
        continue

    change_game_field(user_move, field)
    print_field(field)

    analyze_result = analyze_field(field)
    if analyze_result:
        print(analyze_result)
        break
