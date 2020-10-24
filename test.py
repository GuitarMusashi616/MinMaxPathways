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


if __name__ == "__main__":
    test_new_no_grid()