import numpy as np
import pandas as pd
import tqdm

def split_array_fix_size(input_array, fix_size):
    return [input_array[i:i + fix_size] for i in range(0, len(input_array), fix_size)]

def smart_chunks(lst, n):
    """Choose chunking method based on deviation from the desired chunk size."""
    chunk_count = len(lst) // n
    remainder = len(lst) % n

    # Calculate the size of the last chunk with the leftover method
    leftover_last_chunk_size = remainder if remainder != 0 else n

    # Calculate the size of the last chunk with the equally spread method
    spread_last_chunk_size = n + 1 if remainder > chunk_count else n

    # If the size of the last chunk with the leftover method is closer to n, use chunks_chunks_if_leftover_list
    if abs(n - leftover_last_chunk_size) <= abs(n - spread_last_chunk_size):
        return chunks_chunks_if_leftover_list(lst, n)

    # Otherwise, use chunks_equally_spread
    else:
        return chunks_equally_spread(lst, n)

def chunks_chunks_if_leftover_list(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def chunks_equally_spread(lst, n):
    """Yield successive n-sized chunks from lst, spreading remainder equally."""
    chunk_count = len(lst) // n
    remainder = len(lst) % n
    iterator = iter(lst)

    full_chunks = []
    for _ in range(chunk_count):
        full_chunks.append([next(iterator) for _ in range(n)])

    for i in range(remainder):
        full_chunks[i % len(full_chunks)].append(next(iterator))

    return full_chunks




