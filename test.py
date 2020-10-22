import pytest
import numpy as np
from random import randint, choice
import time
from grid import *


# all coordinates in Tuple(row: int, col: int)


def state_1():
    state = Grid(10)
    state.grid[1][0] = 1
    state.grid[2][0] = 1
    state.grid[3][0] = 1
    state.grid[1][1] = 1
    state.grid[1][2] = 1
    state.grid[1][3] = 1
    state.grid[1][4] = 1
    state.grid[2][3] = 2
    state.grid[2][4] = 2
    return state


def state_2():
    state = Grid(10)
    state.grid = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 2, 2, 2, 0, 0, 0, 0],
        [0, 1, 2, 0, 0, 2, 0, 0, 0, 0],
        [2, 2, 0, 0, 0, 2, 2, 2, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    ], dtype=np.int8)
    return state


def state_3(simulated_turns=0, n=5):
    state = Grid(n)
    # state.grid = np.array([
    #     [0, 0, 0, 0, 0],
    #     [0, 1, 0, 2, 2],
    #     [0, 1, 2, 0, 0],
    #     [2, 2, 0, 0, 0],
    #     [1, 1, 1, 1, 1],
    # ], dtype=np.int8)

    is_players_turn = True
    for _ in range(simulated_turns):
        moves = state.viable_moves()
        if not moves:
            return state
        r, c = choice(moves)
        if is_players_turn:
            state.grid[r][c] = 1
            is_players_turn = False
        else:
            state.grid[r][c] = 2
            is_players_turn = True
    return state


def within_bounds(grid, coord):
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def get_neighbors(grid, coord, player_num, previous_direction=None):
    dcoords = [(0, 1, Direction.RIGHT), (0, -1, Direction.LEFT), (1, 0, Direction.UP), (-1, 0, Direction.DOWN)]

    assert within_bounds(grid, coord) and grid[coord[0], coord[1]] != 0

    if coord[1] == grid.shape[1] - 1:
        return True

    if previous_direction is not None:
        dcoords.pop(previous_direction)  # corresponds to the opposite direction

    for dr, dc, direction in dcoords:
        r, c = coord[0] + dr, coord[1] + dc
        if within_bounds(grid, (r, c)) and grid[r][c] == player_num:
            # only checking within bounds and not where came from
            # return the coords and their relative direction from this node
            # neighbors.append((r, c, direction))
            result = get_neighbors(grid, (r, c), player_num, direction)
            if result:
                return result


def get_0_column(grid):
    coords = []
    for r in range(len(grid)):
        if grid[r][0] == 1 or grid[r][0] == 2:
            coords.append((r, 0))
    return coords


def test_0_column():
    print()
    state = state_1()
    print(state)
    # checks the 0 column for candidates
    candidate_coords = get_0_column(state.grid)
    assert candidate_coords == [(1, 0), (2, 0), (3, 0), (5, 0), (7, 0), (9, 0)]

    # for each candidate, checks connected nodes
    assert get_neighbors(state.grid, (3, 0), 1) is True
    assert get_neighbors(state.grid, (2, 0), 2) is None


def test_big_complete():
    print()
    state = state_2()
    print(state_2)
    candidate_coords = get_0_column(state.grid)
    get_neighbors(state.grid, candidate_coords[0], 1)


def test_in_last_column():
    print()
    state = state_2()
    print(state_2)
    for _ in range(20):
        r = randint(0, len(state.grid) - 1)
        c = randint(0, len(state.grid) - 1)
        if c == len(state.grid) - 1:
            assert state.in_last_column((r, c)) is True
            # print((r,c))
        else:
            assert state.in_last_column((r, c)) is False


def test_initial_state():
    print()
    init = Grid(5)
    print(init)
    print(init.is_full())
    other = state_2()
    print(other)
    print(other.is_full())
    other.reset_grid(len(other.grid))
    print(other)
    print(other.is_full())
    other.grid = np.array([[1 for _ in range(10)] for _ in range(10)])
    print(other)
    print(other.is_full())


def test_breadth_winner():
    print()
    state = state_2()
    print(state)
    print(state.is_winner_breadth_first())


def test_path_coords():
    print()
    state = state_2()
    print(state)
    print(state.get_path_coords())
    group = set()
    print()
    print(state.get_connected((1, 3), group))
    print(group)
    path_groups = state.get_path_groups()
    print(path_groups)
    print(state.count_unique_columns(path_groups))


def test_static_eval():
    print()
    state = Grid(10)
    print(state)
    print(state.static_evaluation())
    print(state.static_evaluation())

    for _ in range(20):
        r, c = choice(state.viable_moves())
        state.grid[r][c] = randint(1, 2)

    print(state)
    print(state.static_evaluation())
    print(state.static_evaluation())


def test_clone():
    print()
    state = state_2()
    clone = state.clone()

    print(state)
    print(clone)
    print("Initial Grids")

    for _ in range(20):
        r, c = choice(state.viable_moves())
        state.grid[r][c] = randint(1, 2)

    print("1st grid changed")
    print(state)
    print(clone)

    for _ in range(20):
        r, c = choice(clone.viable_moves())
        clone.grid[r][c] = randint(1, 2)

    print("2nd grid changed")
    print(state)
    print(clone)


def test_minmax():
    print()
    state = state_3(5)
    coord, score = state.minmax()
    print(state)
    print(coord, score)


def depth_limit_example(n):
    print()
    state = state_3(5)
    state.depth = 0
    coord, score = state.minmax(depth_limit=n)
    print(state)
    print(coord, score)


def time_depth_limit_difference():
    c_5 = time.perf_counter()
    depth_limit_example(math.inf)
    c_4 = time.perf_counter()
    depth_limit_example(4)
    c_3 = time.perf_counter()
    depth_limit_example(3)
    c_2 = time.perf_counter()
    depth_limit_example(2)
    c_1 = time.perf_counter()
    depth_limit_example(1)
    c_0 = time.perf_counter()

    print(f"inf depth: {c_4-c_5}")
    print(f"depth 4: {c_3 - c_4}")
    print(f"depth 3: {c_2- c_3}")
    print(f"depth 2: {c_1 - c_2}")
    print(f"depth 1: {c_0 - c_1}")


def test_alpha_beta():
    print()
    state = state_3(5)
    coord, score = state.alpha_beta()
    print(state)
    print(coord, score)


if __name__ == '__main__':
    t1 = time.perf_counter()
    test_minmax()
    t2 = time.perf_counter()
    test_alpha_beta()
    t3 = time.perf_counter()

    print(t2-t1)
    print(t3-t2)

