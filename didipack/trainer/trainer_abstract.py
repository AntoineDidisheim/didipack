import sys
from didipack.parameters import Params
import pandas as pd
import re
from matplotlib import pyplot as plt
from typing import Tuple
from abc import ABC, abstractmethod


class BaseTrainer(ABC):
    def __init__(self, par: Params):
        self.par = par
        self.verbose = True

    def train_at_time_t(self, x: pd.DataFrame, y: pd.DataFrame,ids:pd.Series,times:pd.Series, t_index_for_split, hyper_parameters_set: dict = {}):
        x_train, y_train, x_val, y_val, x_test, y_test = self._split_data(x, y,ids=ids, times=times, t_index=t_index_for_split)

        # first we need to run the validation procedure.
        best_hyper_params = self._validation_procedure(x_train, y_train, x_val, y_val, hyper_parameters_set)

        # final training
        x = pd.concat([x_train, x_val], axis=0)
        y = pd.concat([y_train, y_val], axis=0)
        y_oos, y_ins = self._train_model_and_predict(x_train=x, y_train=y, x_test=x_test,hyper_params=best_hyper_params)
        y_test['pred'] = y_oos
        if self.par.train.save_ins:
            y['pred'] = y_ins
        else:
            y = pd.DataFrame()
        return y_test, y

    def _split_and_index(self, x: pd.DataFrame, y: pd.DataFrame, ids: pd.Series, times: pd.Series, start, end) -> Tuple[
        pd.DataFrame, pd.DataFrame]:
        indices = (times >= start) & (times < end)
        x_sub = x.loc[indices, :]
        y_sub = y.loc[indices, :]
        ids_sub = ids.loc[indices]
        times_sub = times.loc[indices]
        y_sub = y_sub.set_index([times_sub, ids_sub])
        return x_sub, y_sub

    def _split_data(self, x: pd.DataFrame, y: pd.DataFrame, ids: pd.Series, times: pd.Series, t_index) \
            -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        if self.par.train.T_train < 0:
            start_train = times.min()
        else:
            start_train = t_index - self.par.train.T_train


        end_train = t_index - self.par.train.T_val
        end_test = t_index + self.par.train.testing_window

        x_train, y_train = self._split_and_index(x, y, ids, times, start_train, end_train)
        x_val, y_val = self._split_and_index(x, y, ids, times, end_train, t_index)
        x_test, y_test = self._split_and_index(x, y, ids, times, t_index, end_test)
        return x_train, y_train, x_val, y_val, x_test, y_test

    def _train_model_and_predict(self, x_train: pd.DataFrame, y_train: pd.DataFrame, x_test: pd.DataFrame,
                                 hyper_params: dict):
        self._train_model(x=x_train, y=y_train, hyper_params=hyper_params)
        y_oos = self._predict(x_test)
        if self.par.train.save_ins:
            y_ins = self._predict(x_train)
        else:
            y_ins = None
        return y_oos, y_ins

    @abstractmethod
    def _validation_procedure(self, x_train: pd.DataFrame, y_train: pd.DataFrame, x_val: pd.DataFrame,
                              y_val: pd.DataFrame, hyper_parameters_set : dict) -> dict:
        best_hypper = {}
        return best_hypper

    @abstractmethod
    def _predict(self, x):
        y = x.sum(1)
        return y

    @abstractmethod
    def _train_model(self, x: pd.DataFrame, y: pd.DataFrame, hyper_params: dict):
        if self.verbose:
            print('Model trained', flush=True)




if __name__ == "__main__":
    try:
        grid_id = int(sys.argv[1])
        model_id = int(sys.argv[2])
        print('Running with args', grid_id, flush=True)
    except:
        print('Debug mode on local machine', flush=True)
        grid_id = 0
        model_id = 5

