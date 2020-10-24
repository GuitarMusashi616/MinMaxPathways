from nogrid import *
from node import *


def minmax(grid, func=max, depth_limit=math.inf):
    root_node = Node(func=func, depth_limit=depth_limit)
    root_node.minmax(grid)
    index = root_node.scores.index(root_node.pick)

    return root_node.moves[index], root_node.pick[0], root_node.pick[1]


def play_game(n=4):
    grid = create_grid(n)
    is_players_turn = get_who_moves_first()
    game_over = False
    while not game_over:
        if is_players_turn:
            get_human_player_move(grid, minmax)
            is_players_turn = False
        else:
            generate_computer_player_move(grid, minmax)
            is_players_turn = True
        game_over = check_for_a_win(grid)


if __name__ == "__main__":
    play_game(4)