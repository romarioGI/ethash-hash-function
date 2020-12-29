import copy

from common import HASH_BYTES, WORD_BYTES, sha3_512, fnv, MIX_BYTES, get_size as common_get_size

DATASET_BYTES_INIT = 2 ** 30  # bytes in dataset at genesis
DATASET_BYTES_GROWTH = 2 ** 23  # dataset growth per epoch
DATASET_PARENTS = 256  # number of parents of each dataset element


def calc_dataset_item(cache, i):
    n = len(cache)
    r = HASH_BYTES // WORD_BYTES
    # initialize the mix
    mix = copy.copy(cache[i % n])
    mix[0] ^= i
    mix = sha3_512(mix)
    # fnv it with a lot of random cache nodes based on i
    for j in range(DATASET_PARENTS):
        cache_index = fnv(i ^ j, mix[j % r])
        mix = list(map(fnv, mix, cache[cache_index % n]))
    return sha3_512(mix)


def calc_dataset(full_size, cache):
    for i in range(full_size // HASH_BYTES):
        yield calc_dataset_item(cache, i)


def get_size(block_number):
    return common_get_size(block_number, DATASET_BYTES_INIT, DATASET_BYTES_GROWTH, MIX_BYTES)
