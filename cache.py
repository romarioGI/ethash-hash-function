from common import HASH_BYTES, sha3_512, get_size as common_get_size

CACHE_BYTES_INIT = 2 ** 24  # bytes in cache at genesis
CACHE_BYTES_GROWTH = 2 ** 17  # cache growth per epoch
CACHE_MULTIPLIER = 1024  # Size of the DAG relative to the cache
CACHE_ROUNDS = 3  # number of rounds in cache production


def get_size(block_number):
    return common_get_size(block_number, CACHE_BYTES_INIT, CACHE_BYTES_GROWTH, HASH_BYTES)


def make(cache_size, seed):
    def xor(a, b):
        return a ^ b

    def init():
        # Sequentially produce the initial dataset
        last = sha3_512(seed)
        yield last
        for _ in range(1, n):
            last = sha3_512(last)
            yield last

    n = cache_size // HASH_BYTES

    cache = list(init())

    # Use a low-round version of randmemohash
    for _ in range(CACHE_ROUNDS):
        for i in range(n):
            u = (i - 1 + n) % n
            v = cache[i][0] % n
            cache[i] = sha3_512(list(map(xor, cache[u], cache[v])))

    return cache
