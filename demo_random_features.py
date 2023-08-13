import tqdm
import os
import sys
import pandas as pd
import pickle
import numpy as np
from didipack.create_rf.RandomFeaturesGenerator import RandomFeaturesSpecs, RandomFeaturesGenerator
from didipack.create_rf.gen_rf_factors import generate_random_features_in_blocks

def load_fake_data(n=5, months=10, p=3):
    # Generate dates
    date_rng = pd.date_range(start='1990-01-01', periods=months, freq='M')

    # Generate firm IDs
    firm_ids = list(range(1, n+1))

    # Create a multi-index from the product of dates and firm IDs
    index = pd.MultiIndex.from_product([date_rng, firm_ids], names=['date', 'firm_id'])

    # Create the raw_features DataFrame with random values
    raw_features = pd.DataFrame(np.random.randn(len(index), p), index=index, columns=[f'feature_{i+1}' for i in range(p)])

    # Create the returns DataFrame with random values
    returns = pd.DataFrame(np.random.randn(len(index), 1), index=index, columns=['returns'])

    return raw_features, returns


if __name__ == '__main__':
    try:
        grid_id = int(sys.argv[1])
        print('START RUNNING', grid_id, flush=True)
    except:
        print('Debug mode on local machine')
        grid_id = 0

    save_dir = 'rf_chunks/'
    para_id = 0
    para_nb_of_list_group = 10
    start_seed = 0
    gamma_list = [0.5,0.6,0.7,0.8,0.9,1.0]
    gamma_list = [0.5]
    # voc_grid = [100, 200, 360, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]
    voc_grid = [50,100, 200, 360, 500, 1000]
    max_rf = 1000
    block_size_for_generation = 26
    build_factor = True

    os.makedirs(save_dir,exist_ok=True)
    raw_signal, ret = load_fake_data(n=100,months=120)

    list_of_specs = [RandomFeaturesSpecs(distribution_parameters=[0.0, gamma]) for gamma in gamma_list]
    random_features_generator = RandomFeaturesGenerator(rf_spec_list=list_of_specs,build_factor=build_factor)

    for para_id in range(para_nb_of_list_group):
        print('##########', save_dir,flush=True)
        # if os.path.exists(save_dir + f'rf_chunk_{para_id}.p'):
        if False:
            print(f'Already ran {para_id}',flush=True)
        else:
            print(f'Starts running {para_id}',flush=True)
            generate_random_features_in_blocks(
                x_mat=raw_signal.values,
                y_mat=ret.values,
                date_ids=ret.reset_index()['date'].values.reshape(-1, 1),
                nb_of_random_features_total=max_rf,
                block_size_for_generation=block_size_for_generation,
                save_dir=save_dir,
                random_features_generator=random_features_generator,
                start_seed=start_seed,
                voc_grid=voc_grid,
                para_nb_of_list_group=para_nb_of_list_group,
                para_id=para_id,
                save_results=True
            )



























