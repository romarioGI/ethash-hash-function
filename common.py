import hashlib
import pickle

EPOCH_LENGTH = 30000  # blocks per epoch
HASH_BYTES = 64  # hash length in bytes
WORD_BYTES = 4  # bytes in word
MIX_BYTES = 128  # width of mix
FNV_PRIME = 16777619
FNV_MOD = 2 ** 32


def fnv(v1: int, v2: int):
    return ((v1 * FNV_PRIME) ^ v2) % FNV_MOD


def fnv_arr(arr):
    fnv_hash = 0
    for a in arr:
        fnv_hash = fnv(fnv_hash, a)
    return fnv_hash


# из-за неточности вычисления корня, большие полные квадраты могу быть восприняты как простые числа
def is_prime(x):
    for i in range(2, int(x ** 0.5)):
        if x % i == 0:
            return False
    return True


def get_size(block_number, bytes_init, bytes_growth, bytes_):
    sz = bytes_init + bytes_growth * (block_number // EPOCH_LENGTH)
    sz -= bytes_
    while not is_prime(sz // bytes_):
        sz -= 2 * bytes_
    return sz


def sha3_256(x):
    return hash_words(lambda v: hashlib.sha3_256(v).digest(), x)


def sha3_512(x):
    return hash_words(lambda v: hashlib.sha3_512(v).digest(), x)


# получается лишнее перекладывание информации: list[int] ~> bytes ~> list[int]
# а всё потому, что не сделали отдельную структуру, которая поддерживает операции над целыми числами,
# но при этом компактно хранится в виде массива байтов
def hash_words(h, x):
    if isinstance(x, list):
        x = list_to_bytes(x)
    y = h(x)
    return bytes_to_list(y)


def list_to_bytes(hl: list) -> bytes:
    # right zero padding
    def rz_pad(s, length: int):
        return s + bytes(max(0, length - len(s)))

    # в исходнике это encode_int -- крайне не читаемый метод
    # эта функция эквивалентна функции из описания
    def int_to_bytes(num: int) -> bytes:
        bs = []
        while num > 0:
            bs.append(num & 255)
            num >>= 8
        return bytes(bs)

    return b''.join(map(lambda x: rz_pad(int_to_bytes(x), WORD_BYTES), hl))


def bytes_to_list(hb: bytes) -> list:
    def bytes_to_int(bs: bytes) -> int:
        num = 0
        for b in reversed(bs):
            num = (num << 8) | int(b)
        return num

    return [bytes_to_int(hb[i:i + WORD_BYTES]) for i in range(0, len(hb), WORD_BYTES)]


def serialize(data, file_name):
    with open(file_name, 'wb') as write_file:
        pickle.dump(data, write_file)


def deserialize(file_name):
    with open(file_name, 'rb') as read_file:
        return pickle.load(read_file)
