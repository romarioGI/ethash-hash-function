import cache
import common
import hashimoto
import nist_tests


def make_and_serialize_cache():
    sz = cache.get_size(0)
    seed = bytes(64)
    c = cache.make(sz, seed)
    common.serialize(c, 'cache')


cache_ = common.deserialize('cache')


def hash_():
    # INPUT
    block_number = 0
    header = b'header'
    nonce = b'nonce'
    # END INPUT
    res = hashimoto.hashimoto_light(block_number, cache_, header, nonce)
    print('bytes:         ', res)
    print('bytes (digit): ', list(res))
    print('hex:           ', res.hex())
    print('\nTests')
    length = len(res) * 8
    print('frequency_test', nist_tests.frequency_test(res, length))
    for block_sz in range(1, 17, 3):
        print(f'frequency_block_test_{block_sz}', nist_tests.frequency_block_test(res, length, block_sz))


def get_test_seq():
    s = '1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000'
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')


def frequency_test_example():
    print(nist_tests.frequency_test(get_test_seq(), 100))


def frequency_block_test_example():
    print(nist_tests.frequency_block_test(get_test_seq(), 100, 10))
