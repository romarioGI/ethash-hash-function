from common import HASH_BYTES, WORD_BYTES, sha3_256, sha3_512, list_to_bytes, MIX_BYTES, fnv, fnv_arr
from dataset import calc_dataset_item, get_size as dataset_get_size

ACCESSES = 64  # number of accesses in hashimoto loop


def hashimoto(header: bytes, nonce: bytes, full_size, dataset_lookup):
    n = full_size // HASH_BYTES
    w = MIX_BYTES // WORD_BYTES
    mix_hashes = MIX_BYTES // HASH_BYTES
    seed = sha3_512(header + nonce[::-1])
    # start the mix with replicated s
    mix = []
    for _ in range(mix_hashes):
        mix.extend(seed)
    # mix in random dataset nodes
    for i in range(ACCESSES):
        p = fnv(i ^ seed[0], mix[i % w]) % (n // mix_hashes) * mix_hashes
        new_data = []
        for j in range(mix_hashes):
            new_data.extend(dataset_lookup(p + j))
        mix = list(map(fnv, mix, new_data))
    # compress mix
    compress_mix = []
    for i in range(0, len(mix), WORD_BYTES):
        compress_mix.append(fnv_arr(mix[i:i + WORD_BYTES]))
    return list_to_bytes(sha3_256(seed + compress_mix))


def hashimoto_light(block_number, cache, header, nonce):
    full_size = dataset_get_size(block_number)
    return hashimoto(header, nonce, full_size, lambda x: calc_dataset_item(cache, x))


def hashimoto_full(dataset, header, nonce):
    full_size = len(dataset) * HASH_BYTES
    return hashimoto(header, nonce, full_size, lambda x: dataset[x])
