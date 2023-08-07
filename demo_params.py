import numpy as np
import pandas as pd
import statsmodels.api as sm
import didipack as didi

# the idea of the parameter class is to centralize the parameters of your project in a single class
# since its a class you can create several set of parameters and save them separatly
# you can overite the name function so that the name of the parameter is an automatic function of the parameter set
# you can also use it to loop through different values of the parameters with the function update_param_grid


##################
# example, creating the class
##################
# To use it you need to create our own parameters using inheritance.

# First create a set of little class containing the parameters, here are two examples.
class ParamsModelA:
    def __init__(self):
        self.alpha = 1
        self.beta = 0.5
        self.gamma = 21

class ParamsModelB:
    def __init__(self):
        self.alpha = 0.8
        self.nu = 1
        self.opti = 'adam'
        self.gamma = 21
        self.missing_params = 'nope'

# now create the main Params class which inherit didi.ParamsBasis
class Params(didi.Params):
    def __init__(self):

        self.name_detail = ''
        self.name = ''
        self.seed = 12345

        # put here a link to the little class so the model are included
        self.a = ParamsModelA()
        self.b = ParamsModelB()

        self.update_model_name()

    def update_model_name(self):
        # you can overwrite the model name to have an automatic name, function of some key parameters
        # here is an example
        self.name = self.name_detail + 'Aalpha_' + str(self.a.alpha) + 'gamma_' + str(self.b.gamma) + 'Type_' + self.b.opti

##################
# examples of applicaiton
##################
# creating a parameters
par1 = Params()
# note that one of the advantage of this organisation in sub-classes is that it allows multiple parameter with the same name
# here for example both model A and B have an alpha parameters, but they are stored separatly.
print('par1.a.alpha',par1.a.alpha,'par1.b.alpha',par1.b.alpha,)
# this is quite usefull when you want to follow the notation of multiple papers or you have to many parameters for the greek alphabet.

# you can modify some parameters of this specific instatiations
par1.a.alpha = 8
par1.b.gamma = -1
# change the name after changing parameters in case we want to save it
par1.update_model_name()

# creating another set of parameters
par2 = Params() # this is initiated with the default parameters
print('The two parameter set have different values ')
print('par2.a.alpha',par2.a.alpha,'par1.a.alpha',par1.a.alpha)
print('\n','\n')

# printing the summary with the print_values function, can be usefull if you want to check what the model looks like
par1.print_values()
print('\n','\n')

# saving the parameters
par1.save(save_dir='save/'+par1.name)
par2.save(save_dir='save/'+par2.name)
# note that saving create a folder and put a parameter object in it. This is ideal if you want to save results for different parameter set
# whenever you come back to your folder of result, all is always contained in this par object.

# to load a parameter you first create a new parameter object
load_par_1 = Params()
# then you just load with the directory
load_par_1.load('save/'+par1.name)
# the parameter object is backward compatible
# if you update your project and add parameters you can still load it
# it will load all the parameters, set the new one to default value and print a warning.
# in this example, I saved a version of the parameters that did not had the b.missing_params values
# here is what happen when the parameter is loaded
par_missing = Params()
par_missing.load('save/missing')

##################
# grids
##################

# This last function is quite usefull to do some parameter girds search through the parameter class.
# You first create a list of list as below
# each list in the list of list is of dimension 3
# first the name of the sub param clas
# second the name of the parameter
# third the list of parameter you want the frid to come through
par = Params()
grid = [
    ['a','alpha',[0.1,0.2,0.3]],
    ['b','alpha',[0.1,0.2,0.3]],
    ['b','gamma',[1,2]]
]

# the grid has 18 combinations
# you can update the parameters to one paraticular combinations with the command
# the function update_param take
par.update_param_grid(grid, 0)

# the loop below goes through all combinations and print the values to show how the update works
print(("{:>10}"*3).format('a.alpha', 'b.alpha','b.gamma'))
print('-'*35)
for i in range(18):
    par.update_param_grid(grid,i)
    print(("{:>10}"*3).format(par.a.alpha, par.b.alpha,par.b.gamma))