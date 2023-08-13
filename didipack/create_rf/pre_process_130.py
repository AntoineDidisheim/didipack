import os
import pandas as pd

JKP_signals = ['cowc_gr1a', 'oaccruals_at', 'oaccruals_ni', 'taccruals_at', 'taccruals_ni',
               'capex_abn', 'debt_gr3', 'fnl_gr1a', 'ncol_gr1a', 'nfna_gr1a', 'noa_at',
               'aliq_at', 'at_gr1', 'be_gr1a', 'capx_gr1', 'capx_gr2',
               'capx_gr3', 'coa_gr1a', 'col_gr1a', 'emp_gr1', 'inv_gr1', 'inv_gr1a',
               'lnoa_gr1a', 'mispricing_mgmt', 'ncoa_gr1a', 'nncoa_gr1a', 'noa_gr1a',
               'ppeinv_gr1a', 'ret_60_12', 'sale_gr1', 'sale_gr3', 'saleq_gr1',
               'seas_2_5na', 'age', 'aliq_mat', 'at_be', 'bidaskhl_21d', 'cash_at',
               'netdebt_me', 'ni_ivol', 'rd_sale', 'rd5_at', 'tangibility', 'z_score',
               'beta_60m', 'beta_dimson_21d', 'betabab_1260d', 'betadown_252d',
               'chcsho_12m', 'earnings_variability', 'eqnetis_at', 'fcf_me', 'ivol_capm_21d',
               'ivol_capm_252d', 'ivol_ff3_21d', 'ivol_hxz4_21d', 'netis_at', 'ocfq_saleq_std',
               'rmax1_21d', 'rmax5_21d', 'rvol_21d', 'turnover_126d', 'zero_trades_126d',
               'zero_trades_21d', 'zero_trades_252d', 'prc_highprc_252d', 'resff3_12_1',
               'resff3_6_1', 'ret_12_1', 'ret_3_1', 'ret_6_1', 'ret_9_1', 'seas_1_1na',
               'dsale_dinv', 'dsale_drec', 'dsale_dsga', 'niq_at_chg1', 'niq_be_chg1', 'niq_su',
               'ocf_at_chg1', 'qmj_safety', 'ret_12_7', 'sale_emp_gr1', 'saleq_su', 'seas_1_1an',
               'sti_gr1a', 'dolvol_var_126d', 'ebit_bev', 'ebit_sale', 'f_score', 'intrinsic_value',
               'ni_be', 'niq_be', 'o_score', 'ocf_at', 'ope_be', 'ope_bel1',
               'turnover_var_126d', 'at_turnover', 'cop_at',
               'cop_atl1', 'dgp_dsale', 'gp_at', 'gp_atl1', 'mispricing_perf', 'ni_inc8q',
               'niq_at', 'op_at', 'op_atl1', 'opex_at', 'qmj', 'qmj_growth', 'qmj_prof',
               'sale_bev', 'tax_gr1a', 'corr_1260d', 'coskew_21d', 'dbnetis_at',
               'kz_index', 'lti_gr1a', 'ni_ar1', 'pi_nix', 'seas_11_15an', 'seas_11_15na',
               'seas_16_20an', 'seas_16_20na', 'seas_2_5an', 'seas_6_10an', 'seas_6_10na',
               'ami_126d', 'dolvol_126d', 'market_equity', 'prc', 'rd_me',
               'iskew_capm_21d', 'iskew_ff3_21d', 'iskew_hxz4_21d', 'ret_1_0', 'rmax5_rvol_21d',
               'rskew_21d', 'at_me', 'be_me', 'bev_mev', 'debt_me', 'div12m_me', 'ebitda_mev',
               'eq_dur', 'eqnpo_12m', 'eqnpo_me', 'eqpo_me', 'ni_me', 'ocf_me', 'sale_me']

future_return_column_name = 'ret_exc_lead1m'

def pre_process_raw_signals_130(base_folder, save_dir=None, start_date ='19630101', end_date ='20191231',tolerance_for_nan_in_one_row =0.3,max_nb_of_predictor=130):

    # load the data
    JKP_filename = os.path.join(base_folder, 'usa_factor_data.csv')
    # prepare the target directory to save the resulting folder
    if save_dir is None:
        save_dir = base_folder + '/130_signal/'
    os.makedirs(save_dir, exist_ok=True)

    # select the columns of interest
    id_col = ['id', 'eom', 'size_grp']
    cols_read = id_col + JKP_signals + [future_return_column_name]

    # load the csv
    df = pd.read_csv(JKP_filename, usecols=cols_read, parse_dates=['eom'])

    # drop nano
    df = df.loc[df['size_grp'] != 'nano', :]

    # drop low and upper date
    ind = (df['eom'] >= pd.to_datetime(start_date)) & (df['eom'] <= pd.to_datetime(end_date))
    df = df.loc[ind, :].reset_index(drop=True)

    if max_nb_of_predictor > 0:
        # check missing values across the full sample
        # and keep only max_nb_of_predictor with fewer number of missing values
        all = pd.isna(df[JKP_signals]).mean()
        all.name = 'all'
        df = df.loc[~pd.isna(df[future_return_column_name]), :]
        keep_col = list(pd.isna(df[JKP_signals]).mean().sort_values().head(max_nb_of_predictor).index)
        df = df.loc[:, id_col + keep_col + [future_return_column_name]]

    # drop the rows with more than tolerance_for_nan_in_one_row o Nan
    ind = pd.isna(df[keep_col]).mean(1) <= tolerance_for_nan_in_one_row
    df = df.loc[ind, :].reset_index(drop=True)
    df = df.rename(columns={'eom': 'date'})

    # save per size group in pickle to faciltate
    for size in df['size_grp'].unique():
        df.loc[df['size_grp'] == size, :].drop(columns='size_grp').to_pickle(save_dir + size + '.p')

if __name__ == '__main__':
    # example of one of the pre-processing
    pre_process_raw_signals_130(base_folder='work/PRTNR/EPFL/CDM/smalamud/complexmodels/virtualcomplexityeverywhere_data/')
