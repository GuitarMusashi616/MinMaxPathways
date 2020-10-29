from nogrid import *
from ui import *


def main():
    n = get_integer_input("What grid size (N) shall we use?\n", 3, 15)
    d = get_integer_input("What depth limit shall we use? (0 for auto)\n", 0, 100)

    is_players_turn = get_yes_or_no("Want to go first? (y/n)\n")
    is_fancy_ui = get_yes_or_no("Use fancy UI? (y/n)\n")

    grid = create_grid(n, is_players_turn)
    constant = get_time_constant(4, is_players_turn, True)

    if is_fancy_ui:
        play_ui(grid, is_players_turn, constant, d)
    else:
        play_game(grid, is_players_turn, constant, d)


if __name__ == '__main__':
    main()