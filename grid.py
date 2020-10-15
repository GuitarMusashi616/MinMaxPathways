import numpy as np


class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


class Grid:
    """Methods and states for representing the grid, used for minmax algorithm"""

    def __init__(self, n):
        self.grid = Grid.create_grid(n)

    def __repr__(self):
        string = ''
        for r in range(len(self.grid) - 1, -1, -1):
            for c in range(len(self.grid)):
                if self.grid[r][c] == 1:
                    string += 'H'
                elif self.grid[r][c] == 2:
                    string += 'M'
                else:
                    string += '-'
            string += '\n'
        return string

    @staticmethod
    def create_grid(n):
        grid = np.zeros((n, n), dtype=np.int8)
        for r in range(grid.shape[0] - 1, -1, -1):
            for c in range(grid.shape[1]):
                if not r % 2 and c % 2:  # H: even row odd column
                    grid[r][c] = 1
                elif r % 2 and not c % 2:  # M: odd row even column
                    grid[r][c] = 2
        return grid

    def reset_grid(self, n):
        self.grid = Grid.create_grid(n)

    def within_bounds(self, coord):
        return 0 <= coord[0] < self.grid.shape[0] and 0 <= coord[1] < self.grid.shape[1]

    def in_last_column(self, coord):
        # assert type(coord) is tuple and len(coord) == 2, "Coord not valid"
        if coord[1] == len(self.grid) - 1:
            return True
        return False

    def is_winner_breadth_first(self):
        """Returns the coord from any link of coords that stretch from the 0th column to the last column"""
        queue = self.get_0_column()
        exclude = set(queue)
        while queue:
            r, c = queue.pop(0)
            if self.in_last_column((r, c)):
                return r, c
            for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # left, right, down, up
                new_coord = r + dr, c + dc
                if self.within_bounds(new_coord) and new_coord not in exclude:
                    # check number
                    if self.grid[r + dr][c + dc] == self.grid[r][c]:  # both a 1 or both a 2
                        queue.append(new_coord)
                        exclude.add(new_coord)

    def get_0_column(self):
        """Returns a list of coords of the 1s or 2s in the 0th column of the grid"""
        coords = []
        for r in range(len(self.grid)):
            if self.grid[r][0] == 1 or self.grid[r][0] == 2:
                coords.append((r, 0))
        return coords

    def is_full(self):
        """Returns true if all cells in grid have a 1 or 2"""
        for r in range(len(self.grid) - 1, -1, -1):
            for c in range(len(self.grid)):
                if self.grid[r][c] == 0:
                    return False
        return True

    def check_for_a_win(self):
        # M path from left to right - M wins
        # H path from left to right - H wins
        # Every cell full and there is no winner - Draw
        pass
