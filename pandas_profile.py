# memory_profilerは微妙． 自分でpsutilsとasizeofで調べていくのが良い （実験と沿う結果になるのはこっち）
# @profile
def main():

    import time
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import psutil
    from psutil._common import bytes2human
    from pympler.asizeof import asizeof

    p = psutil.Process()

    x = np.linspace(1,10**4,10)
    for n in x:
        measure_this = pd.DataFrame(np.zeros(shape=(int(n),int(n))))
        print("Mem of df: ", bytes2human(asizeof(measure_this)))

        memory = p.memory_full_info()
        print("Mem of process before del: ", bytes2human(memory.rss))
        print("Mem of process before del: ", bytes2human(memory.vms))

        del measure_this
        memory = p.memory_full_info()
        print("Mem of process after del: ", bytes2human(memory.rss))
        print("Mem of process after del: ", bytes2human(memory.vms))

    return

if __name__ == '__main__':
    main()

# %load_ext memory_profiler
# %memit main()
# ! mprof plot -o "pandas_profile_result"
