from common import HASH_BYTES, sha3_512, get_size as common_get_size

CACHE_BYTES_INIT = 2 ** 24  # bytes in cache at genesis
CACHE_BYTES_GROWTH = 2 ** 17  # cache growth per epoch
CACHE_MULTIPLIER = 1024  # Size of the DAG relative to the cache
CACHE_ROUNDS = 3  # number of rounds in cache production


def get_size(block_number):
    return common_get_size(block_number, CACHE_BYTES_INIT, CACHE_BYTES_GROWTH, HASH_BYTES)


def make(cache_size, seed: bytes):
    def init():
        # Sequentially produce the initial dataset
        last = sha3_512(seed)
        yield last
        for _ in range(1, n):
            last = sha3_512(last)
            yield last

    def algo_round():
        def xor(a, b):
            return a ^ b

        # Use a low-round version of rand-memo-hash
        for i in range(n):
            u = (i - 1 + n) % n
            v = (u + (int.from_bytes(cache[u], 'little') % (n - 1))) % n
            cache[i] = sha3_512(bytes(map(xor, cache[u], cache[v])))

    n = cache_size // HASH_BYTES
    cache = list(init())

    for _ in range(CACHE_ROUNDS):
        algo_round()

    return cache
