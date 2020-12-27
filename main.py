pass

'''block_number = 0
seed = bytes(32)
cache_size = cache.get_size(block_number)
c = cache.make(cache_size, seed)
common.serialize(c, "cache_0_32.json")'''

'''cache = common.deserialize("cache_0_32.json")

sz = dataset.get_size(0)
d = dataset.calc_dataset(sz, cache)

common.serialize(d, f"dataset_0_cache_0_32.json")'''
