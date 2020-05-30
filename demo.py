import pandas as pd
import numpy as np
import statsmodels.api as sm
from enum import Enum
import didipack as didi
df = pd.DataFrame(np.random.uniform(size=(100, 11)), columns=['A', 'B', 'C', 'Z', 'D', 'E', 'F', 'G', 'H', 'I', 'Y'])
df['C']= 1
m1 = sm.OLS(endog=df['Y'], exog=df[['A', 'B', 'C','Z', 'I']]).fit()
m2 = sm.OLS(df['Y'], df[['A', 'B', 'C', 'D']]).fit()
m3 = sm.OLS(df['Y'], df[['A', 'B', 'C', 'E', 'F']]).fit()
df['yl'] = df['Y']>0.5

m1 = sm.Logit(endog=df['yl'], exog=df[['A', 'B', 'C','Z', 'I']]).fit()
m2 = sm.Logit(df['yl'], df[['A', 'B', 'C', 'D']]).fit()
m3 = sm.Logit(df['yl'], df[['A', 'B', 'C', 'E', 'F']]).fit()



table_1 = didi.TableReg(hide_list=['I','E','F','Z'], order=['C', 'D'])
table_1.set_col_groups([['first two',1,2], ['last three',3,5]])
table_1.add_reg(m1, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 3}])
table_1.add_reg(m2, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 1}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 5}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 1}])
table_1.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 2}])
table_1.save_tex()
self = table_1

table_2 = didi.TableReg(show_only_list=['C'])
table_2.add_reg(m1)
table_2.add_reg(m2)
table_2.add_reg(m3)
table_2.add_reg(m3)
table_2.add_reg(m3)



table_3 = didi.TableReg(show_only_list=['D'])
table_3.set_col_groups([['One col',1,1], ['another',2,2], ['one more',3,3],['the rest',4,5]])
table_3.add_reg(m1, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 3}])
table_3.add_reg(m2, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 1}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'No'}, {'Market controls': 5}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 1}])
table_3.add_reg(m3, blocks=[{'area FE': 'Yes', 'I FE': 'Yes'}, {'Market controls': 2}])

#
table_list = [table_1,table_2, table_3]
name_list = ['long regressions','short regressions','final short regressions']
didi.TableReg.create_panel_of_tables(table_list,name_list)