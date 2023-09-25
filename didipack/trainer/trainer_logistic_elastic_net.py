import sys
import pandas as pd
from didipack.trainer.trainer_abstract import BaseTrainer
from didipack.utils_didi.ridge import run_efficient_ridge
import numpy as np
from didipack import Params
from sklearn.linear_model import LogisticRegression



class TrainerLogisticElasticNet(BaseTrainer):
    def __init__(self, par: Params, para=None):
        super().__init__(par)
        self.m = None
        self.par = par
        self.para = para


    def _predict(self, x):
        return self.m.predict_proba(x)[:,-1]

    def _train_model(self, x: pd.DataFrame, y: pd.DataFrame, hyper_params):
        self.m = LogisticRegression(C=hyper_params['shrinkage'][0], penalty='elasticnet', l1_ratio=hyper_params['l1_ratio'][0], solver='saga', fit_intercept=True, n_jobs=self.para)
        self.m.fit(x,y)

    def _validation_procedure(self, x_train: pd.DataFrame, y_train: pd.DataFrame, x_val: pd.DataFrame,
                              y_val: pd.DataFrame, hyper_parameters_set):

        # if no grid is defiend, default is 0.5
        try:
            list_of_l1_ratio= self.par.train.l1_ratio
        except:
            list_of_l1_ratio = [0.5]

        perf = {}
        comb = {}

        k=0
        for l1_ratio in list_of_l1_ratio:
            for shrinkage in self.par.train.shrinkage_list:
                hyp = {'shrinkage':[shrinkage],'l1_ratio':[l1_ratio]}
                print('Just before the analysis',flush=True)
                self._train_model(x=x_train,y=y_train,hyper_params=hyp)
                perf[k] = self.m.score(X=x_val,y=y_val)
                comb[k]=hyp
                k+=1
                print('Ran One analysis',k,flush=True)

        best_hype = comb[pd.Series(perf).idxmax()]
        print('Select best hype', best_hype,flush=True)
        return best_hype



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
    self = TrainerLogisticElasticNet(par)

    N = 1000
    P = 100
    np.random.seed(1)
    fake_data = pd.DataFrame(np.random.normal(size=(N,P)))
    y = pd.DataFrame(np.sign(fake_data.mean(1)))
    dates = pd.Series(np.arange(N))
    ids = dates.copy()

    y_test, _ = self.train_at_time_t(x=fake_data,y=y,ids=ids,times=dates,t_index_for_split=100)

