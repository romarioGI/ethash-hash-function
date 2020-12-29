"""
реализованы тесты по спецификации NIST: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf
для байтовых последовательностей
"""
from math import erfc

from scipy.special import gammainc


def frequency_test(sequence: bytes, length: int):
    """
    частотный тест
    """
    N = len(sequence) * 8
    if length > N:
        raise Exception
    N = length
    s = 0
    cnt = 0
    for b in sequence:
        for i in range(8):
            if cnt >= N:
                continue
            if b & (1 << i) == 0:
                s -= 1
            else:
                s += 1
            cnt += 1
    s = abs(s) / (N ** 0.5)
    p_val = erfc(s / (2.0 ** 0.5))
    return {
        'p_val': p_val,
        'is rnd': p_val >= 0.01
    }


def frequency_block_test(sequence: bytes, length: int, block_size: int):
    """
    частотный блочный тест
    """
    N = len(sequence) * 8
    if length > N:
        raise Exception
    N = length
    N //= block_size
    pi = [0] * N
    cnt = 0
    for b in sequence:
        for i in range(8):
            if cnt >= N * block_size:
                continue
            if b & (1 << i) != 0:
                pi[cnt // block_size] += 1
            cnt += 1
    pi = [x / block_size for x in pi]
    khi_obs_sqr = 4 * block_size * sum(map(lambda x: (x - 0.5) ** 2, pi))
    p_val = 1 - gammainc(N / 2, khi_obs_sqr / 2)
    return {
        'p_val': p_val,
        'is rnd': p_val >= 0.01
    }


def runs_test(sequence: bytes, length: int):
    """
    тест "дырок"
    """
