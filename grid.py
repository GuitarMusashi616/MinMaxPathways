import numpy as np


class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


class Node:
    def __init__(self, grid, coord, action_resulting_in_node=None):
        assert grid.within_bounds(coord), "coordinates are not in the range of the grid"
        # todo: modify actions on initialization - no going out of bounds, no going back to last coord, no going onto occupied space
        self.coord = coord
        self.action_resulting_in_node = action_resulting_in_node

    def actions(self):
        if self.action_resulting_in_node == Direction.LEFT:
            return [Direction.LEFT, Direction.DOWN, Direction.UP]
        elif self.action_resulting_in_node == Direction.RIGHT:
            return [Direction.RIGHT, Direction.DOWN, Direction.UP]
        elif self.action_resulting_in_node == Direction.DOWN:
            return [Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        elif self.action_resulting_in_node == Direction.UP:
            return [Direction.RIGHT, Direction.LEFT, Direction.UP]
        return []

    def child(self, grid, action):
        if action == Direction.LEFT:
            pass



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

    def within_bounds(self, coord):
        return 0 <= coord[0] < self.grid.shape[0] and 0 <= coord[1] < self.grid.shape[1]

    def actions(self, coord):
        pass

    def child_node(self, action):
        pass

    def in_last_column(self, coord):
        # assert type(coord) is tuple and len(coord) == 2, "Coord not valid"
        if coord[1] == len(self.grid)-1:
            return True
        return False

    def is_winner_breadth_first(self):
        frontier = []
        explored = {}
        while frontier:
            node = frontier.pop(0)
            explored.add(node)
            for action in node.actions():
                child = node.child(self, action)
                if child not in explored or frontier:
                    if self.in_last_column(child):
                        return child
                    frontier.append(child)

    def get_0_column(self):
        coords = []
        for r in range(len(self.grid)):
            if self.grid[r][0] == 1 or self.grid[r][0] == 2:
                coords.append((r, 0))
        return coords
