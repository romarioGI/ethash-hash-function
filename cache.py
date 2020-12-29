from common import HASH_BYTES, sha3_512, get_size as common_get_size

CACHE_BYTES_INIT = 2 ** 24  # bytes in cache at genesis
CACHE_BYTES_GROWTH = 2 ** 17  # cache growth per epoch
CACHE_MULTIPLIER = 1024  # Size of the DAG relative to the cache
# а в тексте сказано, что два раунда
CACHE_ROUNDS = 3  # number of rounds in cache production


def get_size(block_number):
    return common_get_size(block_number, CACHE_BYTES_INIT, CACHE_BYTES_GROWTH, HASH_BYTES)


# реализация rand-memo-hash не соответствует описанию http://www.hashcash.org/papers/memohash.pdf
# баг это или фича?
# про seed информации нет
def make(cache_size: int, seed):
    def xor(a, b):
        return a ^ b

    n = cache_size // HASH_BYTES

    # Sequentially produce the initial dataset
    cache = [sha3_512(seed)]
    for i in range(1, n):
        cache.append(sha3_512(cache[-1]))

    # Use a low-round version of rand-memo-hash
    for _ in range(CACHE_ROUNDS):
        for i in range(n):
            v = cache[i][0] % n
            cache[i] = sha3_512(list(map(xor, cache[(i - 1 + n) % n], cache[v])))

    return cache
