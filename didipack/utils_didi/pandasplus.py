import numpy as np
import pandas as pd
import tqdm
from abc import ABC, abstractmethod

class PandasPlus:

    @staticmethod
    def get_memory_usage_in_gb(df:pd.DataFrame):
        total_mem_usage_bytes = df.memory_usage(deep=True).sum()
        total_mem_usage_gb = total_mem_usage_bytes / 1024 ** 3
        return total_mem_usage_gb

    @staticmethod
    def winzorize_series(s, p=5):
        """
        Winzorizes a pandas Series by p percent on both sides of the distribution.

        Parameters:
        - s: The pandas Series to winzorize.
        - p: The percentage to winzorize on both sides. Defaults to 5%.

        Returns:
        - The winzorized Series.
        """
        lower = s.quantile(p / 100)
        upper = s.quantile(1 - p / 100)

        return s.clip(lower=lower, upper=upper)

    @staticmethod
    def get_ym(s:pd.Series):
        '''
        get yms from pandas
        :param s:
        :return:
        '''
        return s.dt.year*100 + s.dt.month

    @staticmethod
    def get_yw(s: pd.Series) -> pd.Series:
        '''
        Get unique year-week identifier from a datetime pandas Series.

        :param s: A datetime-like pandas Series
        :return: A Series with unique year-week identifiers
        '''
        return s.dt.year * 100 + s.dt.isocalendar().week

    @staticmethod
    def weighted_sum_pandas_series(w: pd.Series, target: pd.Series, gb: pd.Series):
        return (target * w).groupby(gb).sum() / w.groupby(gb).sum()


    @staticmethod
    def normalize_by_gp_rank(s: pd.Series, gp: pd.Series):
        '''
        Rank columns in a way that sums to 1.


        :param df:
        :param col_list:
        :param groupby_name:
        :return:
        '''
        t = s.groupby(gp.values).transform('rank') - 1
        t_n = s.groupby(gp.values).transform('count') - 1
        return (t / t_n).values - 0.5

    @staticmethod
    def normalize_series_between_with_minmax(series):
        return 2 * ((series - series.min()) / (series.max() - series.min())) - 1