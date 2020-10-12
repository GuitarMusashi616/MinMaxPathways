import numpy as np


class Grid:
    """Methods and states for representing the grid, used for minmax algorithm"""

    def __init__(self, n):
        self.grid = np.zeros((n, n), dtype=np.int8)

    def __repr__(self):
        string = ''
        for r in range(len(self.grid)-1,-1,-1):
            for c in range(len(self.grid)):
                string += str(self.grid[r][c]) if self.grid[r][c] != 0 else '-'
            string += '\n'
        return string