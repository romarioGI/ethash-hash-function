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
    а в спецификации NIST очепятка: неправильно посчитан тау в примере
    """
    N = len(sequence) * 8
    if length > N:
        raise Exception
    N = length
    pi = 0
    cnt = 0
    last = -1
    v_obs = 0
    for b in sequence:
        for i in range(8):
            if cnt >= N:
                continue
            cur_bit = b & (1 << i) != 0
            if cur_bit:
                pi += 1
            if cur_bit != last:
                v_obs += 1
            last = cur_bit
            cnt += 1
    pi /= N
    tau = 2 / (N ** 0.5)
    if abs(pi - 0.5) >= tau:
        p_val = 0
    else:
        p_val = erfc(abs(v_obs - 2 * N * pi * (1 - pi)) / (2 * (2 * N) ** 0.5 * pi * (1 - pi)))
    return {
        'p_val': p_val,
        'is rnd': p_val >= 0.01
    }
