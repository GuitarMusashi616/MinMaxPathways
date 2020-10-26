from nogrid import *
import time


def test_new_no_grid():
    grid = generate_grid(4, 0)
    print(grid)
    t1 = time.perf_counter()
    print(minmax(grid))
    t2 = time.perf_counter()
    print(alpha_beta(grid))
    t3 = time.perf_counter()
    # print(alpha_beta(grid, depth_limit=5))
    t4 = time.perf_counter()
    print(t2 - t1)
    print(t3 - t2)
    print(t4 - t3)
    print(grid)


def test_deepening():
    grid = generate_grid(4, 0)
    t1 = time.perf_counter()
    print(minmax(grid, depth_limit=8))
    t2 = time.perf_counter()
    print(minmax(grid, depth_limit=7))
    t3 = time.perf_counter()
    print(minmax(grid, depth_limit=6))
    t4 = time.perf_counter()
    print(minmax(grid, depth_limit=5))
    t5 = time.perf_counter()
    print(minmax(grid, depth_limit=4))
    t6 = time.perf_counter()
    print(minmax(grid, depth_limit=3))
    t7 = time.perf_counter()

    print(t2 - t1)
    print(t3 - t2)
    print(t4 - t3)
    print(t5 - t4)
    print(t6 - t5)
    print(t7 - t6)


def test_speed():
    grid = create_grid(5)
    t1 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=7)
    print(coord, score, depth)
    t2 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=15)
    print(coord, score, depth)
    t3 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=12)
    print(coord, score, depth)
    t4 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=9)
    print(coord, score, depth)
    t5 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=6)
    print(coord, score, depth)
    t6 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=3)
    print(coord, score, depth)

    print(f"Time: {t2 - t1}")
    print(f"Time: {t3 - t2}")
    print(f"Time: {t4 - t3}")
    print(f"Time: {t5 - t4}")
    print(f"Time: {t6 - t5}")


def test_one():
    grid = create_grid(8)
    t1 = time.perf_counter()
    coord, score, depth = alpha_beta(grid, func=min, depth_limit=6)
    print(coord, score, depth)
    t2 = time.perf_counter()
    print(f"Time: {t2 - t1}")


def test_random_move():
    grid = create_grid(4)
    print(grid)
    generate_random_move(grid, 1)
    print(grid)
    generate_random_move(grid, 2)
    print(grid)
    generate_random_move(grid, 2)
    print(grid)
    generate_random_move(grid, 1)
    print(grid)


def test_random_turns():
    grid = create_grid(4)
    print(grid)
    generate_random_turns(grid, 1, 5)
    print(grid)


def time_algo_at_depth(grid, d, is_alpha_beta=False):
    t1 = time.perf_counter()
    string = "Minmax" if not is_alpha_beta else "Alpha_Beta"
    print(string)
    coord, score, depth = alpha_beta(grid, func=min, alpha=None, beta=None, depth_limit=d) if not is_alpha_beta else alpha_beta(grid, func=min, depth_limit=d)
    t2 = time.perf_counter()
    print(f"Time: {t2 - t1}")
    print(coord, score, depth)


def test_time_predictions(n, turns):
    grid = create_grid(n)
    generate_random_turns(grid, 1, turns)
    move_count = len(viable_moves(grid))
    print(f"grid: {grid.shape[0]}x{grid.shape[1]}, moves: {move_count}")
    time_algo_at_depth(grid, math.inf)
    time_algo_at_depth(grid, math.inf, True)


def check_constants():
    print('Minmax')
    print(get_time_constant(2))
    print(get_time_constant(3))
    print(get_time_constant(4))
    print('Alpha_beta')
    print(get_time_constant(2, True))
    print(get_time_constant(3, True))
    print(get_time_constant(4, True))


if __name__ == "__main__":
    tM = get_time_constant(3)
    tA = get_time_constant(3, True)
    for i in range(9,3,-1):
        grid = create_grid(5)
        generate_random_turns(grid, 1, i)
        move_count = len(viable_moves(grid))
        print(f'Minmax Prediction: {time_prediction(tM, move_count)}')
        t1 = time.perf_counter()
        alpha_beta(grid, func=min, alpha=None, beta=None)
        t2 = time.perf_counter()
        print(f'Actual: {t2-t1}')

        print(f'Alpha_Beta Prediction: {time_prediction(tA, move_count, True)}')
        t1 = time.perf_counter()
        alpha_beta(grid, func=min)
        t2 = time.perf_counter()
        print(f'Actual: {t2-t1}')







