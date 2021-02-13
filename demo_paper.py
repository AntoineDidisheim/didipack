import didipack as didi
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import statsmodels.api as sm

##################
# Creating a new paper with LatexPaper
##################

# define the paper maine directory (can be relative or abolute path)
paper = didi.LatexPaper(dir_='paper_demo')
# Creating the paper itself with a given title, author name and some default sections (non-mandatory)
paper.create_paper('paper',title = "Example of an automatic paper", author ="Antoine Didisheim", sec = ['Activation function','Random regressions'])

##################
# Creating few figures for the results section
##################

x = np.arange(-3,3,0.01)
y_sig = 1/(1+np.exp(-x))
y_swish = x / (1 + np.exp(-x))
y_relu = np.maximum(x,0)
# 1v1
plt.plot(x,y_sig,label='Sigmoid',color=didi.DidiPlot.COLOR[0],linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.grid(True)
# note that I use the directory for figure save in the paper object and used the default .png.
plt.savefig(paper.dir_figs+'sigmoid.png')
plt.close()

plt.plot(x,y_relu,label='Relu',color=didi.DidiPlot.COLOR[0],linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.grid(True)
plt.savefig(paper.dir_figs+'relu.png')
plt.close()

plt.plot(x, y_swish, label='Swish', color=didi.DidiPlot.COLOR[0], linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.grid(True)
plt.savefig(paper.dir_figs+'swish.png')
plt.close()

#2v2
plt.plot(x,y_sig,label='Sigmoid',color=didi.DidiPlot.COLOR[0],linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.plot(x,y_relu,label='Relu',color=didi.DidiPlot.COLOR[1],linestyle=didi.DidiPlot.LINE_STYLE[1])
plt.grid(True)
plt.legend()
plt.savefig(paper.dir_figs+'relu_v_sigmoid.png')
plt.close()


plt.plot(x,y_swish,label='Swish',color=didi.DidiPlot.COLOR[0],linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.plot(x,y_relu,label='Relu',color=didi.DidiPlot.COLOR[1],linestyle=didi.DidiPlot.LINE_STYLE[1])
plt.grid(True)
plt.legend()
plt.savefig(paper.dir_figs+'relu_v_swish.png')
plt.close()

# 3v3
plt.plot(x,y_swish,label='Swish',color=didi.DidiPlot.COLOR[0],linestyle=didi.DidiPlot.LINE_STYLE[0])
plt.plot(x,y_sig,label='Sigmoid',color=didi.DidiPlot.COLOR[1],linestyle=didi.DidiPlot.LINE_STYLE[1])
plt.plot(x,y_relu,label='Relu',color=didi.DidiPlot.COLOR[2],linestyle=didi.DidiPlot.LINE_STYLE[2])
plt.grid(True)
plt.legend()
plt.savefig(paper.dir_figs+'all_v_all.png')
plt.close()

##################
# Populate the 'Activation function' section with these figures
##################
# We reset the section to avoid appending the same text twice when we run the code twice.
paper.create_new_sec('Activation function',r"% Start of the activation function section"+'\n')

#We add a bit of text
text = "In this section, we illustrate the difference between popular activation functions."
paper.append_text_to_sec('Activation function',text)

# We add a single figure
paper.append_fig_to_sec(fig_names=['all_v_all.png'],sec_name='Activation function',
                        main_caption="The figure above show all three activation functions in the same graph.")

# The figure comes with automatic labels that can be used in texts. The main caption is stor a fig:<overall_label>
# If no overall_label is defined, default is the first figure name
text = r"Figure \ref{fig:all_v_all} includes all three activation function discussed here in a single plot. " \
       r"We are now going to show the same lines in individual plot"
paper.append_text_to_sec('Activation function',text)

# We now add two figure side by side
paper.append_fig_to_sec(fig_names=['relu_v_swish','relu_v_sigmoid'], sec_name='Activation function',
                        overall_label='2_2', # if left empty, default would be first firgure name
                        fig_captions=['ReLu vs Swish', 'ReLu vs Sigmoid'],  # you can add individual caption to each figure (leave empty for no label)
                        main_caption="The figure above sigmoid and swish activations functions compared to ReLu")

# The figure also comes with inidivudal label for subfigure: fig:<overall_label>_id (id being letters)
text = r"Figure \ref{fig:2_2} show swish and sigmoid function versus relu in two different graphs. Figure \ref{fig:2_2_a} " \
       r"shows relu vs swish, while figure \ref{fig:2_2_b} shows relu vs sigmoid."
paper.append_text_to_sec('Activation function',text)


# We now add thres figures side by side with default size
paper.append_fig_to_sec(fig_names=['relu','swish','sigmoid'], sec_name='Activation function',
                        overall_label='3_3_default', # if left empty, default would be first firgure name
                        main_caption="The figure above shows three graph side by side with default setting")
# We can also add the same figure with another size pre-defined size
paper.append_fig_to_sec(fig_names=['relu','swish','sigmoid'], sec_name='Activation function',
                        size="0.45\linewidth", # this would set each subfigure to take 45% of avaialable vertical space
                        overall_label='3_3_custom_size', # if left empty, default would be first firgure name
                        main_caption="The figure above shows three graph side by side with custom size")


##################
# Constructing some tables
##################

# create random data
df = pd.DataFrame(data = np.random.normal(size=(100,4)),columns=['A','B','C','D'])
df['A'] = df['A']*0.7 + df['B']*0.3 + np.random.normal(0,0.1,size=100)

# create descriptive statistics and save it in the correct directory
df.describe().round(4).to_latex(paper.dir_tables+'desc.tex')

# run some regressions to create one more table
table = didi.TableReg()
for c in ['B','C','D']:
    m = sm.OLS(df['A'],df[[c]]).fit()
    table.add_reg(m)
m = sm.OLS(df['A'],df[['B','C']]).fit()
table.add_reg(m)
m = sm.OLS(df['A'],df[['B','D']]).fit()
table.add_reg(m)
m = sm.OLS(df['A'],df[['C','D']]).fit()
table.add_reg(m)
m = sm.OLS(df['A'],df[['B','C','D']]).fit()
table.add_reg(m)
table.save_tex(paper.dir_tables+'reg.tex')

##################
# Adding those tables to the random regressions section
##################
# As before, we rest the section to avoid appending the same text twice when we run the code twice.
paper.create_new_sec("Random regressions",r"% Start of the random regressions section"+'\n')
#start the section on a fresh page
paper.append_text_to_sec("Random regressions",r'\clearpage')
# add the descriptive function table
paper.append_table_to_sec('desc',sec_name="Random regressions",
                          caption="The table below show descriptive statistics of our pseudo-random example")
# we add the regressions but the table is a big too big...
paper.append_table_to_sec('reg',sec_name="Random regressions",
                          caption="The table below show the results of our regressions without a resizebox. The table is too big for the page.")
# the size parameter can be used to define the table size as percentage of pagewidth
# The default label is tables:<table_name> but it can be overwritten with overall_caption
paper.append_table_to_sec('reg',sec_name="Random regressions",
                          resize=1.0,
                          overall_caption='second_reg_table',
                          caption="The table below show the results of our regression with a resize parameter equal t 1.0")

# to see the results just go to paper demo and compile (for example on linux with pdflatex with the command : pdflatex paper.tex)






