import numpy as np
from random import choice
import math
import time


class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


def play_game(n=4, suggestion=False):
    grid = create_grid(n)
    is_players_turn = get_who_moves_first()
    game_over = False
    constant = get_time_constant(4, True)
    while not game_over:
        if is_players_turn:
            get_human_player_move(grid, alpha_beta, suggestion)
            is_players_turn = False
        else:
            generate_computer_player_move(grid, alpha_beta, constant, 10)
            is_players_turn = True
        game_over = check_for_a_win(grid)


def get_integer_input(input_str='Type an integer: ', lower_bound=0, upper_bound=math.inf):
    x = None
    while True:
        try:
            x = input(input_str)
            x = int(x)
            assert lower_bound <= x <= upper_bound, f"Integer must be in the range [{lower_bound}, {upper_bound}]"
            break
        except ValueError:
            print('Please type an integer')
        except AssertionError as e:
            print(e)
    return x


def create_grid(n):
    if not n:
        return None
    grid = np.zeros((n, n), dtype=np.int8)
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1]):
            if not r % 2 and c % 2:  # H: even row odd column
                grid[r][c] = 1
            elif r % 2 and not c % 2:  # M: odd row even column
                grid[r][c] = 2
    return grid


def generate_grid(n=5, simulated_turns=0):
    grid = create_grid(n)

    is_players_turn = True
    for _ in range(simulated_turns):
        moves = viable_moves(grid)
        if not moves:
            return grid
        r, c = choice(moves)
        if is_players_turn:
            grid[r][c] = 1
            is_players_turn = False
        else:
            grid[r][c] = 2
            is_players_turn = True
    return grid


def print_grid(grid):
    string = ''
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid)):
            if grid[r][c] == 1:
                string += 'H'
            elif grid[r][c] == 2:
                string += 'M'
            else:
                string += '-'
        string += '\n'
    print(string)


def get_who_moves_first():
    # prompt user "want to go first"
    letter = None
    while not letter:
        try:
            letter = input("Want to go first? (y/n)\n")
            assert type(letter) == str, "input must be a string"
            letter = letter.lower()
            assert letter == 'y' or letter == 'n', "input must be a y or an n"
        except AssertionError as e:
            print(e)
        # if False then skip 1st turn
    if letter == 'y':
        return True
    elif letter == 'n':
        return False


def within_bounds(grid, coord):
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def in_last_column(grid, coord):
    # assert type(coord) is tuple and len(coord) == 2, "Coord not valid"
    if coord[1] == len(grid) - 1:
        return True
    return False


def is_winner_breadth_first(grid):
    """Returns the coord from any link of coords that stretch from the 0th column to the last column"""
    queue = get_0_column(grid)
    exclude = set(queue)
    while queue:
        r, c = queue.pop(0)
        if in_last_column(grid, (r, c)):
            return r, c
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # left, right, down, up
            new_coord = r + dr, c + dc
            if within_bounds(grid, new_coord) and new_coord not in exclude:
                # check number
                if grid[r + dr][c + dc] == grid[r][c]:  # both a 1 or both a 2
                    queue.append(new_coord)
                    exclude.add(new_coord)


def get_0_column(grid):
    """Returns a list of coords of the 1s or 2s in the 0th column of the grid"""
    coords = []
    for r in range(len(grid)):
        if grid[r][0] == 1 or grid[r][0] == 2:
            coords.append((r, 0))
    return coords


def is_full(grid):
    """Returns true if all cells in grid have a 1 or 2"""
    for r in range(len(grid) - 1, -1, -1):
        for c in range(len(grid)):
            if grid[r][c] == 0:
                return False
    return True


def check_for_a_win(grid):
    # M path from left to right - M wins
    # H path from left to right - H wins
    # Every cell full and there is no winner - Draw
    coord = is_winner_breadth_first(grid)
    if coord:
        print_grid(grid)
        if grid[coord[0]][coord[1]] == 1:
            print("You Win!")
        elif grid[coord[0]][coord[1]] == 2:
            print("You Lose!")
        return True
    elif is_full(grid):
        print_grid(grid)
        print("Draw!")
        return True
    return False


def viable_moves(grid):
    moves = []
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1]):
            if grid[r][c] == 0:
                moves.append((r, c))
    return moves


def get_human_player_move(grid, strategy, suggestion=False):
    moves = viable_moves(grid)
    print_grid(grid)
    print(f"Options: " + str(moves))
    if suggestion:
        print(f"Best Option: " + str(strategy(grid, func=max)))

    r, c = None, None
    is_valid_move = False
    # not occupied and within bounds
    while not is_valid_move:
        r = get_integer_input('Row: ', 0, len(grid) - 1)
        c = get_integer_input('Col: ', 0, len(grid) - 1)
        if (r, c) in moves:
            is_valid_move = True
        else:
            print("Move is not valid, try another option")

    grid[r][c] = 1
    print()


def generate_computer_player_move(grid, strategy, constant, target_secs):
    print_grid(grid)
    d = get_depth_limit(target_secs, constant, len(viable_moves(grid)))
    coord, score, final_depth = strategy(grid, func=min, depth_limit=d)
    r, c = coord
    grid[r][c] = 2
    print(f"Computer picks {r}, {c} for an estimated score of {score}\n")


def generate_random_move(grid: np.array, player: int):
    assert player == 1 or player == 2
    moves = viable_moves(grid)
    r, c = choice(moves)
    grid[r][c] = player


def generate_random_turns(grid: np.array, starting_player: int, turns: int):
    assert starting_player == 1 or starting_player == 2
    player = 2
    if starting_player == 1:
        player = 1

    for _ in range(turns):
        generate_random_move(grid, player)
        if player == 1:
            player = 2
        else:
            player = 1


def get_path_coords(grid, num=2):
    # 1 for human, 2 for computer
    coords = set()
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1]):
            if grid[r][c] == num:
                coords.add((r, c))
    return coords


def get_connected(grid, coord, group):
    r, c = coord
    group.add(coord)
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_coord = r + dr, c + dc
        if within_bounds(grid, new_coord) and new_coord not in group and grid[r + dr][c + dc] == grid[r][c]:
            get_connected(grid, new_coord, group)
    return group


def get_path_groups(grid, num=2):
    path_groups = []
    path_coords = get_path_coords(grid, num)
    while path_coords:
        r, c = path_coords.pop()
        group = set()
        get_connected(grid, (r, c), group)
        for coord in group:
            if coord in path_coords:
                path_coords.remove(coord)
        path_groups.append(group)
    return path_groups


def count_unique_columns(grouped_coords):
    # grouped_coords is a list of sets
    unique_columns_per_set = []
    for subset in grouped_coords:
        subset_column_numbers = set()
        for coord in subset:
            subset_column_numbers.add(coord[1])
        unique_columns_per_set.append(len(subset_column_numbers))
    return max(unique_columns_per_set)
    # future possibility V
    # return sum([math.pow(2, num_unique_columns) for num_unique_columns in unique_columns_per_set])


def static_evaluation(grid):
    # higher score better for human, lower score better for computer
    path_groups_human = get_path_groups(grid, 1)
    path_groups_computer = get_path_groups(grid, 2)
    return count_unique_columns(path_groups_human) - count_unique_columns(path_groups_computer)


def win_loss_eval(grid) -> int or None:
    """returns +1 if human win, -1 if loss, and 0 if draw"""
    coord = is_winner_breadth_first(grid)
    if coord:
        if grid[coord[0]][coord[1]] == 1:
            # human win
            return 1
        elif grid[coord[0]][coord[1]] == 2:
            # computer win
            return -1
    elif is_full(grid):
        # draw
        return 0


def get_time_constant(n, is_alpha_beta=False):
    alpha = None
    beta = None
    if is_alpha_beta:
        alpha = -math.inf
        beta = math.inf
    grid = create_grid(n)
    move_count = len(viable_moves(grid))
    t1 = time.perf_counter()
    alpha_beta(grid, func=min, alpha=alpha, beta=beta)
    t2 = time.perf_counter()
    return time_constant(move_count, t2-t1)


def time_constant(move_count, secs):
    return secs/math.factorial(move_count)


def time_prediction(constant, move_count, d=math.inf):
    operations = math.factorial(move_count)
    if d >= move_count:
        return operations * constant
    else:
        return (operations/math.factorial(move_count-d))*constant


def get_depth_limit(target_secs, constant, move_count):
    if time_prediction(constant, move_count) < target_secs:
        return math.inf

    for d in range(20, 0, -1):
        if time_prediction(constant, move_count, d) <= target_secs:
            return d


def alpha_beta(grid, coord=None, func=max, alpha=-math.inf, beta=math.inf, depth=0, depth_limit=math.inf):
    # Use alpha=None and beta=None to use regular minmax
    assert func == min or func == max

    score = win_loss_eval(grid)
    if isinstance(score, int):
        depth = depth if depth != 0 else 1
        return coord, score*(1/depth), depth

    if depth >= depth_limit:
        return coord, 0, depth

    moves = viable_moves(grid)

    choices = []
    for r, c in moves:
        if func == max:
            grid[r][c] = 1
            _, score, final_depth = alpha_beta(grid, (r, c), min, alpha, beta, depth + 1, depth_limit)
            alpha = max(score, alpha) if alpha is not None else None
            choices.append(((r, c), score, final_depth))
            grid[r][c] = 0
        else:
            grid[r][c] = 2
            _, score, final_depth = alpha_beta(grid, (r, c), max, alpha, beta, depth + 1, depth_limit)
            beta = min(score, beta) if beta is not None else None
            choices.append(((r, c), score, final_depth))
            grid[r][c] = 0
        if alpha is not None and beta is not None and beta <= alpha:
            break

    best_score = func([s[1] for s in choices])
    best_pick = [s[1] for s in choices].index(best_score)
    best_depth = choices[best_pick][2]
    best_coord = choices[best_pick][0]
    return best_coord, best_score, best_depth


if __name__ == '__main__':
    play_game(8)
