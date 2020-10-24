import math
from nogrid import win_loss_eval, viable_moves


class Node:
    def __init__(self, parent=None, func=max, depth=0, depth_limit=math.inf):
        self.parent = parent
        self.children = []
        self.win_loss_draw = None
        self.grid = None
        self.depth = depth
        self.depth_limit = depth_limit
        self.pick = None
        self.choices = {}
        self.func = func

    def __repr__(self):
        if self.win_loss_draw is None:
            return f"NODE @ depth: {self.depth}"
        elif self.win_loss_draw >= 1:
            return f"WIN @ depth: {self.depth}"
        elif self.win_loss_draw <= -1:
            return f"LOSS @ depth: {self.depth}"
        elif self.win_loss_draw == 0:
            return f"DRAW @ depth: {self.depth}"

    def spawn_child(self, func, depth=0, depth_limit=math.inf):
        child = Node(self, func, depth, depth_limit)
        self.children.append(child)
        return child

    def minmax(self, grid):
        assert self.func == max or self.func == min
        # assert self.parent is None

        self.grid = grid.copy()
        score = win_loss_eval(grid)

        if isinstance(score, int):
            # returns if win, loss, or draw (no moves)
            self.win_loss_draw = score * (1 / self.depth)
            return self.win_loss_draw, self.depth

        if self.depth >= self.depth_limit:
            raise ValueError("depth limit needs to be set higher than " + str(self.depth_limit))
            # node.win_loss_draw = 0
            # return coord, 0, node.depth

        moves = viable_moves(grid)
        for r, c in moves:
            if self.func == max:
                grid[r][c] = 1
                child = self.spawn_child(min, self.depth+1, self.depth_limit)
                self.choices[r, c] = child.minmax(grid)
                grid[r][c] = 0
            else:
                grid[r][c] = 2
                child = self.spawn_child(max, self.depth+1, self.depth_limit)
                self.choices[r, c] = child.minmax(grid)
                grid[r][c] = 0

        self.pick = self.func(self.choices.values())
        # the coords are the key to the score and depth, only care about score
        if self.depth == 0:
            print()
        return self.pick


