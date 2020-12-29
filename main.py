import common
import hashimoto

'''sz = cache.get_size(0)
seed = bytes(64)
c = cache.make(sz, seed)
common.serialize(c, 'cache')'''

'''block_number = 0
cache_ = common.deserialize('cache')
header = b'represents the SHA3-256 hash of the RLP representation of a truncated block header, that is, of a header excluding the fields mixHash and nonce'
nonce = b'is the eight bytes of a 64 bit unsigned integer in big-endian order'
res = hashimoto.hashimoto_light(block_number, cache_, header, nonce)
print(common.bytes_to_list(res))'''


