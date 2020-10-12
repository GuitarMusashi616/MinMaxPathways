import pytest
from grid import *


# all coordinates in Tuple(row: int, col: int)

class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


def state_1():
    state = Grid(5)
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


def within_bounds(grid, coord):
    return 0 <= coord[0] < grid.shape[0] and 0 <= coord[1] < grid.shape[1]


def get_neighbors(grid, coord, player_num, previous_direction=None):
    dcoords = [(0, 1, Direction.RIGHT), (0, -1, Direction.LEFT), (1, 0, Direction.UP), (-1, 0, Direction.DOWN)]

    assert within_bounds(grid, coord) and grid[coord[0], coord[1]] != 0

    if coord[1] == grid.shape[1]-1:
        return True

    if previous_direction is not None:
        dcoords.pop(previous_direction) # corresponds to the opposite direction

    for dr, dc, direction in dcoords:
        r, c = coord[0]+dr, coord[1]+dc
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
    assert candidate_coords == [(1, 0), (2, 0), (3, 0)]

    # for each candidate, checks connected nodes
    assert get_neighbors(state.grid, (3, 0), 1) is True
    assert get_neighbors(state.grid, (2, 0), 2) is None





