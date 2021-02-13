from matplotlib import pyplot as plt
import matplotlib.pylab as pylab
import pandas as pd

params = {'axes.labelsize': 14,
          'axes.labelweight': 'bold',
          'xtick.labelsize': 12,
          'ytick.labelsize': 12,
          'axes.titlesize': 12}
pylab.rcParams.update(params)

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class DidiPlot:
    LINE_STYLE = [
        '-', '--', ':', '-.',(0,(1,10)),(0,(5,19))
    ]
    # COLOR = [
    #     'black', 'gray', 'black', 'dimgray'
    # ]

    COLOR = [
        'black', 'blue', 'green', 'red','purple','brown'
    ]