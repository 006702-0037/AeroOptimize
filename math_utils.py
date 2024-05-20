import numpy as np


def convergence(data, precision=0.01):
    best_mean = [0, max(data)]
    cutoffs = round(len(data) * 0.50)

    for c in range(cutoffs):
        for i in np.arange(min(data[c:]), max(data[c:]), precision):
            mean_offset = sum([abs(ii - i) for ii in data[c:]]) / len(data[c:])
            if mean_offset < best_mean[1]:
                best_mean[1] = mean_offset
                best_mean[0] = i

    return best_mean[0]
