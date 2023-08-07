import numpy as np
import time
import pandas as pd

class TicToc:  # simple class to measure the time of various part of the code
    def __init__(self):
        self.start_time = 0

    def tic(self):
        self.start_time = time.time()

    def toc(self, message=''):
        print(f'{message}: in {np.round((time.time() - self.start_time) / 60, 2)}m', flush=True)
        self.tic()


def get_block_sizes(
        number_random_features: int, small_subset_size: int, voc_grid: list = None
) -> list:
    """returns a list of block sizes"""
    block_sizes = (
        np.arange(0, number_random_features, small_subset_size).astype(int).tolist()
    )
    if number_random_features not in block_sizes:
        block_sizes += [number_random_features]

    # if grid point in voc_grid is not in block_sizes, we add them in the block_sizes
    if voc_grid:
        block_sizes = list(set(block_sizes + voc_grid))
    block_sizes.sort()  # sort grid points
    return block_sizes




