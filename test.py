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
    print(alpha_beta(grid, depth_limit=5))
    t4 = time.perf_counter()
    print(t2-t1)
    print(t3-t2)
    print(t4-t3)
    print(grid)


if __name__ == "__main__":
    test_new_no_grid()