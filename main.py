import concurrent.futures
import math
import time

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def main():
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [(executor.submit(is_prime, prime), prime) for prime in PRIMES]
        for future, prime in futures:
            print(prime, future.result())

    finish = time.perf_counter()
    print(finish-start)


def main2():
    start = time.perf_counter()

    results = [(prime, is_prime(prime)) for prime in PRIMES]

    finish = time.perf_counter()

    print(results)
    print(finish - start)


if __name__ == '__main__':
    main2()
    main()