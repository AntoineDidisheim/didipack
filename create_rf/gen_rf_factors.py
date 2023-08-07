import tqdm

try:  # ugly trick so that we can run python Experience1/run_voc.py and in the main Pycharm system
    import sys
    import pathlib

    sys.path.append(str(pathlib.Path(__file__).parent.resolve()).replace('risk_return_tradeoff', ''))
except:
    print("debug on pycharm -i python")

from RandomFeaturesGenerator import RandomFeaturesGenerator
import os
import sys
import pandas as pd
import pickle
import numpy as np
from aux import TicToc, get_block_sizes

def generate_random_features_in_blocks(
        x_mat: np.ndarray,
        y_mat: np.ndarray,
        date_ids: np.ndarray,
        nb_of_random_features_total: int,
        block_size_for_generation: int,
        save_dir: str,
        random_features_generator: RandomFeaturesGenerator,
        start_seed: int =0,
        voc_grid: list = None,
        para_nb_of_list_group:int = None,
        para_id: None = int,
        save_results = True
):
    '''
    Generates either the full matrix for rf (if para_grid is none) or a large chunk of it block by block.
    Save it in the save_dir to be merged latter.
    :param x_mat: input of raw signals (N*T, p)
    :param y_mat: input of corresponding returns (N*T,1)
    :param date_ids: input of dates for each individual row of x_mat (N*T,1)
    :param nb_of_random_features_total: the value of big P, total number of rf you want.
    :param block_size_for_generation: the maximum size of a block. used to generate the random feature block by block
    :param save_dir: the path to directory were to save intermediary results
    :param random_features_generator: RandomFeaturesGenerator object already initialized with the objects you want.
    :param start_seed: seed that correspond to the overall operation
    :param voc_grid: if you want to use a voc grid with some P in it smaller than the max block size, you shuold include a list of it to make sure each chunk is of the right size.

    The next two parameters concerns paralelization in a server
    :param para_nb_of_list_group: if none, we run the full list of block in one go. Otherwise, we split the list in para_nb_of_list_group chunks that can be run in paralel.
    :param para_id: if para_nb_of_list_group is not none, this will define which of the group of the block list should be run. You should iterate over all of this to run the full P.
    
    :param redo_already_computed_block: if false, we only run the batch if it wasn't already save.
    :return: None
    '''
    tictoc = TicToc()
    blocks = get_block_sizes(nb_of_random_features_total, block_size_for_generation, voc_grid=voc_grid)
    os.makedirs(save_dir, exist_ok=True)
    # the list of all individual blocks to run
    to_run = np.arange(0,len(blocks) - 1,1)
    if para_nb_of_list_group is not None:
        # we will split the loop into max(para_grid+1) chunks, and run the para_id th one
        to_run = np.array_split(to_run, para_nb_of_list_group)[para_id]
        print('split into', len(to_run), 'lists',flush=True)

    rf_factors_all = []

    for i_block in tqdm.tqdm(to_run,'Loop of iblock'):
        rf_factors = random_features_generator.generate_random_features_from_list_with_potential_ranking(
            seed=int((start_seed + 1) * 1e3) + i_block,
            batch_nb_rf=blocks[i_block+1]-blocks[i_block],
            # it seems we are generate each number_features_in_subset for each gamma
            date_ids=date_ids,
            y_mat=y_mat,
            x_mat=x_mat,
        )
        rf_factors_all.append(rf_factors)

    rf_factors = pd.concat(rf_factors_all, axis=1)
    if save_results:
        if para_id is not None:
            rf_factors.to_pickle(save_dir+f'rf_chunk_{para_id}.p')
            tictoc.toc(f"Finished and saved 1/{para_id} of the chunks")
        else:
            rf_factors.to_pickle(save_dir+f'rf.p')
            tictoc.toc("Finished and saved")

    return rf_factors


def generate_random_features_in_blocks_if_not_already_ran(
        x_mat: np.ndarray,
        y_mat: np.ndarray,
        date_ids: np.ndarray,
        nb_of_random_features_total: int,
        block_size_for_generation: int,
        save_dir: str,
        random_features_generator: RandomFeaturesGenerator,
        start_seed: int =0,
        voc_grid: list = None,
        para_nb_of_list_group:int = None,
        para_id: None = int,
        save_results = True
):
    # correcting for the missing chunk
    nb_of_random_features_total += block_size_for_generation

    if os.path.exists(save_dir + f'rf_chunk_{para_id}.p'):
        print(f'ALREADY RAN, skip that one {para_id}',flush=True)
    else:
        print(f'Start running {para_id}',flush=True)
        generate_random_features_in_blocks(
            x_mat = x_mat,
            y_mat = y_mat,
            date_ids = date_ids,
            nb_of_random_features_total = nb_of_random_features_total,
            block_size_for_generation = block_size_for_generation,
            save_dir = save_dir,
            random_features_generator = random_features_generator,
            start_seed = start_seed,
            voc_grid = voc_grid,
            para_nb_of_list_group = para_nb_of_list_group,
            para_id = para_id,
            save_results=save_results
        )