import pandas as pd
from linearmodels import PanelOLS
import statsmodels.api as sm
import numpy as np
import didipack as didi

# Example data
np.random.seed(0)
data = pd.DataFrame({'y': np.random.rand(50),
                     'x1': np.random.rand(50),
                     'x2': np.random.rand(50),
                     'entity': np.repeat(np.arange(10), 5),
                     'time': np.tile(np.arange(5), 10)})

data = data.set_index(['entity', 'time'])

# PanelOLS model
mod = PanelOLS.from_formula('y ~ x1 + x2 + EntityEffects', data)
panel_ols_res = mod.fit()

print("PanelOLS Results:")
print(panel_ols_res)


# Preparing data for statsmodels
data = data.reset_index()
data_with_dummies = pd.get_dummies(data, columns=['entity'], drop_first=True)*1

# OLS model
X = data_with_dummies[['x1', 'x2'] + [col for col in data_with_dummies if col.startswith('entity_')]]
X = sm.add_constant(X)  # adding a constant
y = data_with_dummies['y']

model = sm.OLS(y, X)
results = model.fit()

print("\nStatsmodels OLS Results:")
print(results.summary())

table_2 = didi.TableReg()
table_2.add_reg(panel_ols_res)
table_2.add_reg(results)
table_2.add_reg(panel_ols_res)
table_2.save_tex('tex_example/panel.tex')
