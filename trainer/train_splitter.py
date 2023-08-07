import os
import sys
import numpy as np
import pandas as pd
import tqdm
from didipack.parameters import *
from matplotlib import pyplot as plt
from typing import Tuple, List
from utils.general import smart_chunks
from trainer.trainer_ridge import TrainerRidge


def generate_fake_data(N: int = 1000, P: int = 100) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Generates a dataset of fake data for testing purposes.

    Args:
        N (int): The number of rows in the generated data.
        P (int): The number of columns in the generated data.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: A tuple containing the fake data, its mean along the columns, a series representing dates, and a series representing ids.
    """
    fake_data = pd.DataFrame(np.random.normal(size=(N, P)))
    y = pd.DataFrame(fake_data.mean(1))
    dates = pd.Series(np.arange(N))
    ids = dates.copy()

    return fake_data, y, dates, ids


def create_t_ind_index_from_dates_series(dates):
    return dates.drop_duplicates().sort_values().reset_index(drop=True).reset_index().rename(columns={'index':'t_ind'})


def get_start_dates(dates: pd.Series, T_train, testing_window) -> List:
    """
    Gets start dates for training.

    Args:
        dates (pd.Series): A series containing the dates for the data.
        T_train (int): The length of the training period.
        testing_window (int): The length of the testing period.

    Returns:
        List[int]: A list containing the start dates for training.
    """

    start_dates = [dates.min() + T_train]
    while max(start_dates) < max(dates):
        start_dates.append(max(start_dates) + testing_window)

    return start_dates


def get_chunks(start_dates: List[int], nb_chunks: int, temp_save_dir: str) -> Tuple[
    List[Tuple[str, np.ndarray]], List[Tuple[str, np.ndarray]]]:
    """
    Gets chunks of start dates to process.

    Args:
        start_dates (List[int]): A list containing the start dates for training.
        nb_chunks (int): The number of chunks to split the data into.
        temp_save_dir (str): The directory where temporary data is saved.

    Returns:
        Tuple[List[Tuple[str, np.ndarray]], List[Tuple[str, np.ndarray]]]: A tuple containing two lists, one for the chunks that still need to be processed and one for the chunks that have already been processed.
    """
    chunks_of_start_dates = np.array_split(start_dates, nb_chunks)
    chunks_of_start_dates = [(f'chunk_{i}.p', x) for i, x in enumerate(chunks_of_start_dates)]
    processed_chunks = os.listdir(temp_save_dir)

    chunks_still_to_process = []
    chunks_already_processed = []
    for chunk in chunks_of_start_dates:
        if chunk[0] in processed_chunks:
            chunks_already_processed.append(chunk)
        else:
            chunks_still_to_process.append(chunk)

    return chunks_still_to_process, chunks_already_processed


def get_tasks_for_current_node(chunks_still_to_process: List[Tuple[str, np.ndarray]], nb_nodes_total: int,
                               min_nb_chunks_in_cluster: int, grid_id: int) -> List[Tuple[str, np.ndarray]]:
    """
    Gets tasks for the current node.

    Args:
        chunks_still_to_process (List[Tuple[str, np.ndarray]]): A list containing the chunks that still need to be processed.
        nb_nodes_total (int): The total number of nodes.
        min_nb_chunks_in_cluster (int): The minimum number of chunks in a cluster.
        grid_id (int): The id of the current grid.

    Returns:
        List[Tuple[str, np.ndarray]]: A list containing the tasks for the current node.
    """
    to_run_across_nodes = np.array_split(chunks_still_to_process, nb_nodes_total)
    if max([len(x) for x in to_run_across_nodes]):
        to_run_across_nodes = list(smart_chunks(chunks_still_to_process, min_nb_chunks_in_cluster))
        print(f'Splitting in a smart way {[len(x) for x in to_run_across_nodes]}')
    # [len(x) for x in to_run_across_nodes]
    to_run_now = to_run_across_nodes[grid_id]

    return to_run_now






if __name__ == "__main__":
    try:
        grid_id = int(sys.argv[1])
        model_id = int(sys.argv[2])
        print('Running with args', grid_id, flush=True)
    except:
        print('Debug mode on local machine', flush=True)
        grid_id = 0
        model_id = 5

    par = Params()
    par.train.testing_window = 5
    trainer = TrainerRidge(par)
    nb_nodes_total = 5
    verbose = True
    temp_save_dir = './res/temp2/'
    os.makedirs(temp_save_dir, exist_ok=True)

    fake_data, y, dates, ids = generate_fake_data()


    start_dates = get_start_dates(dates, par.train.T_train, par.train.testing_window)
    chunks_still_to_process, chunks_already_processed = get_chunks(start_dates,  par.train.nb_chunks, temp_save_dir)
    if verbose:
        print(f'Already processed {len(chunks_already_processed)}, Still to processed {len(chunks_still_to_process)}')

    to_run_now = get_tasks_for_current_node(chunks_still_to_process, nb_nodes_total, par.train.min_nb_chunks_in_cluster, grid_id)


    # running the analysis
    k = 0
    for chunk in to_run_now:
        k+=1
        df_oos_pred = pd.DataFrame()
        for start_id in tqdm.tqdm(chunk[1],f'Chunks {k} ({chunk[0]}) out of {len(to_run_now)}'):
        # for start_id in chunk[1]:
            y_test, _ = trainer.train_at_time_t(x=fake_data, y=y, ids=ids, times=dates, t_index_for_split=start_id)
            df_oos_pred = pd.concat([df_oos_pred, y_test], axis=0)
        df_oos_pred.to_pickle(temp_save_dir + chunk[0])
