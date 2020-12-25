import dataset
import common


cache = common.deserialize("cache_0_32.json")

sz = dataset.get_size(0)
d = dataset.calc_dataset(sz, cache)

common.serialize(d, f"dataset_0_cache_0_32.json")
