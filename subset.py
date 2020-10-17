import numpy as np
import concurrent.futures
import time
from random import choice


def create_grid(n):
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


def viable_moves(grid):
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not grid[r][c]:
                coords.append((r, c))
    return coords


def get_path_coords(grid, num=2):
    # 1 for human, 2 for computer
    coords = set()
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1]):
            if grid[r][c] == num:
                coords.add((r, c))
    return coords


def within_bounds(grid, coord):
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


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


def determine_score(grid):
    score = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] == 1:
                score += 1
    return score


def retrieve_best_choice(grid, coord):
    # clone and modify grid
    grid_copy = grid.copy()
    grid_copy[coord[0]][coord[1]] = 1
    # determine score of grid
    return coord, static_evaluation(grid_copy)


def main():
    grid = create_grid(5)
    moves = viable_moves(grid)
    for coord in moves:
        print(retrieve_best_choice(grid, coord))


def main2():
    grid = create_grid(5)
    moves = viable_moves(grid)
    # print(moves)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(retrieve_best_choice, grid, coord) for coord in moves]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(finish-start)
    print()

    start2 = time.perf_counter()
    main2()
    finish2 = time.perf_counter()
    print(finish2-start2)
    print()