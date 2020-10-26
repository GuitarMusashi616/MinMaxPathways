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
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
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

    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    print(t5-t4)
    print(t6 - t5)
    print(t7 - t6)


def test_speed():
    grid = create_grid(5)
    t1 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=7)
    print(coord, score, depth)
    t2 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=15)
    print(coord, score, depth)
    t3 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=12)
    print(coord, score, depth)
    t4 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=9)
    print(coord, score, depth)
    t5 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=6)
    print(coord, score, depth)
    t6 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=3)
    print(coord, score, depth)

    print(f"Time: {t2-t1}")
    print(f"Time: {t3-t2}")
    print(f"Time: {t4-t3}")
    print(f"Time: {t5-t4}")
    print(f"Time: {t6-t5}")


def test_one():
    grid = create_grid(8)
    t1 = time.perf_counter()
    coord, score, depth = alpha_beta_tree(grid, func=min, depth_limit=6)
    print(coord, score, depth)
    t2 = time.perf_counter()
    print(f"Time: {t2-t1}")


if __name__ == "__main__":
    test_one()