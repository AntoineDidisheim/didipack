import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import r2_score

class OlsPLus:
    def __init__(self):
        pass

    def sm_with_fixed_effect(self,df,y,x,fix_effect_cols=[], std_error_cluster=None):
        if (std_error_cluster is None) | (std_error_cluster in x):
            temp = df[[y]+x+fix_effect_cols].copy().dropna()
        else:
            temp = df[[y]+x+fix_effect_cols+[std_error_cluster]].copy().dropna()
        temp['y_untr'] = temp[y]
        t = 0
        if len(fix_effect_cols)>0:
            for fe in fix_effect_cols:
                t += temp.groupby(fe)[y].transform('mean')
                temp[y] = temp[y]-t
                for c in x:
                    temp[c] = temp[c]-temp.groupby(fe)[c].transform('mean')

        if std_error_cluster is None:
            m=sm.OLS(temp[y],temp[x]).fit()
        else:
            m=sm.OLS(temp[y],temp[x]).fit(cov_type='cluster',cov_kwds={'groups':temp[std_error_cluster]})


        if len(fix_effect_cols)>0:
            pred=m.predict(temp[x])+t
            r = r2_score(temp['y_untr'],pred)
            m.rsquared = r
            m.rsquared_adj = 1-(1-r)*(temp.shape[0]-1)/(temp.shape[0]-temp.shape[1]-1)
        return m