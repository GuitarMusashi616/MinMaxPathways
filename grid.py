import numpy as np
from random import choice
import math


class Direction:
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


def play_game(n=3):
    grid = Grid(n)
    is_players_turn = grid.get_who_moves_first()
    game_over = False
    while not game_over:
        if is_players_turn:
            grid.get_human_player_move()
            is_players_turn = False
        else:
            grid.get_computer_player_move()
            is_players_turn = True
        game_over = grid.check_for_a_win()


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

    def clone(self):
        result = Grid(5)
        result.grid = self.grid.copy()
        return result

    @staticmethod
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
        coord = self.is_winner_breadth_first()
        if coord:
            print(self)
            if self.grid[coord[0]][coord[1]] == 1:
                print("You Win!")
            elif self.grid[coord[0]][coord[1]] == 2:
                print("You Lose!")
            return True
        elif self.is_full():
            print(self)
            print("Draw!")
            return True
        return False

    def viable_moves(self):
        moves = []
        for r in range(self.grid.shape[0] - 1, -1, -1):
            for c in range(self.grid.shape[1]):
                if self.grid[r][c] == 0:
                    moves.append((r, c))
        return moves

    def get_human_player_move(self):
        moves = self.viable_moves()
        print(self)
        print(f"Options: " + str(moves))
        print(f"Best Option: " + str(self.retrieve_best_choice(func=max)))

        r, c = None, None
        is_valid_move = False
        # not occupied and within bounds
        while not is_valid_move:
            r = get_integer_input('Row: ', 0, len(self.grid) - 1)
            c = get_integer_input('Col: ', 0, len(self.grid) - 1)
            if (r, c) in moves:
                is_valid_move = True
            else:
                print("Move is not valid, try another option")

        self.grid[r][c] = 1
        print()

    def get_computer_player_move(self):
        coord, score = self.retrieve_best_choice(func=min)
        r, c = coord
        self.grid[r][c] = 2
        print(f"Computer picks {r}, {c} for an estimated score of {score}\n")

    def get_path_coords(self, num=2):
        # 1 for human, 2 for computer
        coords = set()
        for r in range(self.grid.shape[0] - 1, -1, -1):
            for c in range(self.grid.shape[1]):
                if self.grid[r][c] == num:
                    coords.add((r, c))
        return coords

    def get_connected(self, coord, group):
        r, c = coord
        group.add(coord)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_coord = r + dr, c + dc
            if self.within_bounds(new_coord) and new_coord not in group and self.grid[r + dr][c + dc] == self.grid[r][c]:
                self.get_connected(new_coord, group)
        return group

    def get_path_groups(self, num=2):
        path_groups = []
        path_coords = self.get_path_coords(num)
        while path_coords:
            r, c = path_coords.pop()
            group = set()
            self.get_connected((r, c), group)
            for coord in group:
                if coord in path_coords:
                    path_coords.remove(coord)
            path_groups.append(group)
        return path_groups

    @staticmethod
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

    def static_evaluation(self):
        # higher score better for human, lower score better for computer
        path_groups_human = self.get_path_groups(1)
        path_groups_computer = self.get_path_groups(2)
        return self.count_unique_columns(path_groups_human) - self.count_unique_columns(path_groups_computer)

    def player_best_next_choice(self):
        # higher score better for player
        moves = self.viable_moves()
        assert moves, "no viable moves left"
        # do move, analyze, undo move
        best_score = -math.inf
        best_coord = None
        for r, c in moves:
            self.grid[r][c] = 1
            score = self.static_evaluation()
            if score > best_score:
                best_score = score
                best_coord = (r, c)
            self.grid[r][c] = 0
        return best_coord, best_score

    def computer_best_next_choice(self):
        # lower score better for computer
        moves = self.viable_moves()
        assert moves, "no viable moves left"
        # do move, analyze, undo move
        best_score = math.inf
        best_coord = None
        for r, c in moves:
            self.grid[r][c] = 2
            score = self.static_evaluation()
            if score < best_score:
                best_score = score
                best_coord = (r, c)
            self.grid[r][c] = 0
        return best_coord, best_score

    def retrieve_best_choice(self, coord=None, func=max):
        assert func == min or func == max
        moves = self.viable_moves()
        if not moves:
            return coord, self.static_evaluation()

        choices = []
        for r,c in moves:
            grid = self.clone()
            if func == max:
                grid.grid[r][c] = 1
                coord, score = grid.retrieve_best_choice((r,c),min)
                choices.append(score)
            else:
                grid.grid[r][c] = 2
                coord, score = grid.retrieve_best_choice((r,c),max)
                choices.append(score)
        return coord, func(choices)



if __name__ == '__main__':
    play_game(4)