import cache
import common
import hashimoto


def make_and_serialize_cache():
    sz = cache.get_size(0)
    seed = bytes(64)
    c = cache.make(sz, seed)
    common.serialize(c, 'cache')


def hash_():
    block_number = 0
    cache_ = common.deserialize('cache')
    header = b'represents the SHA3-256 hash of the RLP representation of a truncated block header, that is, of a header excluding the fields mixHash and nonce'
    nonce = b'is the eight bytes of a 64 bit unsigned integer in big-endian order'
    res = hashimoto.hashimoto_light(block_number, cache_, header, nonce)
    print('bytes:         ', res)
    print('bytes (digit): ', list(res))
    print('hex:           ', res.hex())
