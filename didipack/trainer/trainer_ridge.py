import sys
import pandas as pd
from didipack.trainer.trainer_abstract import BaseTrainer
from didipack.utils_didi.ridge import run_efficient_ridge
import numpy as np
from didipack import Params

class TrainerRidge(BaseTrainer):
    def __init__(self, par: Params):
        super().__init__(par)
        self.beta = None

    def _predict(self, x):
        return x.values @ self.beta.T

    def _train_model(self, x: pd.DataFrame, y: pd.DataFrame, hyper_params):
        beta = run_efficient_ridge(signals=x.values, labels=y.values,shrinkage_list=hyper_params['shrinkage'])
        self.beta= beta

    def _validation_procedure(self, x_train: pd.DataFrame, y_train: pd.DataFrame, x_val: pd.DataFrame,
                              y_val: pd.DataFrame, hyper_parameters_set):
        self.beta = run_efficient_ridge(signals=x_train.values, labels=y_train.values,shrinkage_list=self.par.train.shrinkage_list)
        y_pred = self._predict(x_val)
        val_perf =np.mean(np.square(y_pred-y_val.values),axis=0)
        best_lambda = self.par.train.shrinkage_list[np.argmin(val_perf)]
        print('Select best lambda', best_lambda,flush=True)
        return {'shrinkage':[best_lambda]}



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
    self = TrainerRidge(par)

    N = 1000
    P = 100
    fake_data = pd.DataFrame(np.random.normal(size=(N,P)))
    y = pd.DataFrame(fake_data.mean(1))
    dates = pd.Series(np.arange(N))
    ids = dates.copy()

    y_test, _ = self.train_at_time_t(x=fake_data,y=y,ids=ids,times=dates,t_index_for_split=100)

