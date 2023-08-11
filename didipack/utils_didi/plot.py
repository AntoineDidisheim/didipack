import matplotlib.pyplot as plt

class PlotPlus:
    @staticmethod
    def plot_dual_axis(df, col1, col2, label1=None, label2=None, xlabel = 'Date'):
        fig, ax1 = plt.subplots()

        # Use column names as labels if no labels are provided
        if label1 is None:
            label1 = col1
        if label2 is None:
            label2 = col2

        # Plotting col1 on the first y-axis
        color = 'tab:blue'
        ax1.set_xlabel(xlabel=xlabel)
        ax1.set_ylabel(label1, color=color)
        ax1.plot(df.index, df[col1], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Creating a second y-axis to plot col2
        ax2 = ax1.twinx()

        color = 'tab:red'
        ax2.set_ylabel(label2, color=color)
        ax2.plot(df.index, df[col2], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
