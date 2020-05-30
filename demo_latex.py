import numpy as np
import pandas as pd
import statsmodels.api as sm
import didipack as didi

##################
# Create a data frame t illustrate regressions
##################
runOLS = True
np.random.seed(123)
df = pd.DataFrame(np.random.uniform(size=(100, 11)), columns=['A', 'B', 'C', 'Z', 'D', 'E', 'F', 'G', 'H', 'I', 'Y'])
df['C']= 1

if runOLS:
    m1 = sm.OLS(endog=df['Y'], exog=df[['A', 'B', 'C','Z', 'I']]).fit()
    m2 = sm.OLS(df['Y'], df[['A', 'B', 'C', 'D']]).fit()
    m3 = sm.OLS(df['Y'], df[['A', 'B', 'C', 'E', 'F']]).fit()
else:
    # example with logisitc regressions
    df['Y'] = df['Y']>0.5
    m1 = sm.Logit(endog=df['Y'], exog=df[['A', 'B', 'C','Z', 'I']]).fit()
    m2 = sm.Logit(df['Y'], df[['A', 'B', 'C', 'D']]).fit()
    m3 = sm.Logit(df['Y'], df[['A', 'B', 'C', 'E', 'F']]).fit()


# create a TableReg object
# hide_list list variables that you don't want to appear in the final table
# order put the order of some variable. The one in the list will be at the top, everything else will be appear alphabetically after that
table_1 = didi.TableReg(hide_list=['I','E','F','Z'], order=['C', 'D'])
# col_groups can be added to add an overal name sturcture on the columns. Its a list of list.
# Each list in col_groups must have three input: name of columns, first number (from 1), last column number)
table_1.set_col_groups([['first two',1,2], ['last three',3,5]])
# you can then use add_reg function to add regressions or columns.
# blocks is for additional variable that you want to add at the end. Its a list of dictionaries.
# Each list of dictionary will be separated by a med skip
# Important, you hae to have the same block of blocks keys for each variable in the regression
table_1.add_reg(m1, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 3}])
table_1.add_reg(m2, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 1}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 5}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 1}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 2}])
# save tex produces the tex file
table_1.save_tex('tex_example/single_table.tex')

# creating a new tableReg
# show only list indicate that you want only the variables in the list to appear. Everything else is added to the hidden list
table_2 = didi.TableReg(show_only_list=['C'])
table_2.add_reg(m1)
table_2.add_reg(m2)
table_2.add_reg(m3)
table_2.add_reg(m3)
table_2.add_reg(m3)

table_3 = didi.TableReg(show_only_list=['D'])
# this show how to set a cutom overal name to individual columns
table_3.set_col_groups([['One col',1,1], ['another',2,2], ['one more',3,3],['the rest',4,5]])
table_3.add_reg(m1, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 3}])
table_3.add_reg(m2, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 1}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 5}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 1}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 2}])

##################
# panel table
##################
# to create a list of table separated in panels, use the static function create_panel_of_tables
# the example above is straight forwards.
table_list = [table_1,table_2, table_3]
name_list = ['long regressions','short regressions','final short regressions']
didi.TableReg.create_panel_of_tables(table_list,name_list,save_dir='tex_example/table_with_panel.tex')

##################
# additional function
##################

# you can change at the last minute the name of a few variables in your table with set_rename_dict:
table_1.set_rename_dict({'C':'main variable','A':r'$\gamma$'})
table_1.save_tex('tex_example/renamed_table.tex')

# you can use bottom blocks to add blocks below the R². The example below add some information on the number of firms at the bottom of the table
table_4 = didi.TableReg(show_only_list=['D'])
table_4.set_col_groups([['21 firms',1,3],['Five firm only',4,5]])
table_4.add_reg(m1, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 3}], bottom_blocks=[{'Nb Firm': 21}])
table_4.add_reg(m2, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 1}], bottom_blocks=[{'Nb Firm': 21}])
table_4.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 5}], bottom_blocks=[{'Nb Firm': 21}])
table_4.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 1}], bottom_blocks=[{'Nb Firm': 5}])
table_4.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 2}], bottom_blocks=[{'Nb Firm': 5}])
table_4.save_tex('tex_example/bottom_blocks.tex')

##################
# static parameters
##################
# the main class has a bunch of static parameter that can be modified:
# missing_symbole control what is put in the table when there is no entry in a cell. You can replace it as follow:
didi.TableReg.missing_symbol = '(-)'
# by default, t-stats are shown in parenthesis, you can change this to standard deviations or pvalues as follows
didi.TableReg.par_value = didi.ParValue.TSTAT
didi.TableReg.par_value = didi.ParValue.STD
didi.TableReg.par_value = didi.ParValue.PVALUE

# the default rounding is at 4 digit, as in most jf papers, you can set the rounding up for the parameters and r^2 separately:
didi.TableReg.round = 3
didi.TableReg.round_r2 = 2

# the * in the table are set to capture 10%, 5% and 1%. The following line change this to 5,0.01,0.001
didi.TableReg.sign_tr = [0.05, 0.01, 0.001]

# you can chose not to show the r² or the number of observation
didi.TableReg.show_obs = False
didi.TableReg.show_r2 = True
# by default there is a small skip between the parameter of the regression, and a medskip between groups or blocks. You can change this wit the lines,
didi.TableReg.variable_skip = r'\smallskip'
didi.TableReg.group_skip = r'\smallskip'
# if you don't like toprules and bottome rule you can change them all to hline with
didi.TableReg.equal_lines = True

# let's now create a table to show how this works:
table_1.save_tex('tex_example/new_parameters.tex')
