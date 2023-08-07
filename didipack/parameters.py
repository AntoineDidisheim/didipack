import numpy as np
import itertools
import pandas as pd
import os


class RandomFeaturesParams:
    def __init__(self):
        self.max_rf = 50*1000
        self.gamma_list = [0.5,0.6,0.7,0.8,0.9,1.0]
        self.block_size_for_generation=1000
        self.start_seed=0
        self.voc_grid=[100, 200, 360, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]
        self.para_nb_of_list_group=20
        self.para_id=0


class TrainerParams:
    def __init__(self):
        self.T_train = 360
        self.T_val = 36
        self.testing_window = 1
        self.shrinkage_list = np.linspace(1e-12,10,50)
        self.save_ins = False

        # this is the number of individual saving chunks.
        # by this we mean the number of individual df contianing some oos performance that will be saved before merged.
        # too big and we risk loosing some processing, too small and we will make a mess of the merging process.
        self.nb_chunks = 25
        #
        self.min_nb_chunks_in_cluster = 10

# store all parameters into a single object
class Params:
    def __init__(self):
        self.name_detail = ''
        self.name = ''
        self.seed = 12345
        self.train = TrainerParams()
        self.rf = RandomFeaturesParams()

        self.update_model_name()

    def update_model_name(self):
        # function to overwrite
        self.name = self.name_detail

    def print_values(self):
        """
        Print all parameters used in the model
        """
        for key, v in self.__dict__.items():
            try:
                print('########', key, '########')
                for key2, vv in v.__dict__.items():
                    print(key2, ':', vv)
            except:
                print(v)

    def update_param_grid(self, grid_list, id_comb, verbose = False):
        ind = []
        for l in grid_list:
            t = np.arange(0, len(l[2]))
            ind.append(t.tolist())
        combs = list(itertools.product(*ind))
        if verbose:
            print('comb', str(id_comb + 1), '/', str(len(combs)))
        c = combs[id_comb]

        for i, l in enumerate(grid_list):
            self.__dict__[l[0]].__dict__[l[1]] = l[2][c[i]]

    def save(self, save_dir, file_name='/parameters.p'):
        # simple save function that allows loading of deprecated parameters object
        # first we create the dir if it doesn't exists already
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)


        df = pd.DataFrame(columns=['key', 'value'])

        for key, v in self.__dict__.items():
            try:
                for key2, vv in v.__dict__.items():
                    temp = pd.DataFrame(data=[str(key) + '_' + str(key2), vv], index=['key', 'value']).T
                    df = df.append(temp)

            except:
                temp = pd.DataFrame(data=[key, v], index=['key', 'value']).T
                df = pd.concat([df,temp],axis=0)
        df.to_pickle(save_dir + file_name)

    def load(self, load_dir, file_name='/parameters.p'):
        # simple load function that allows loading of deprecated parameters object
        df = pd.read_pickle(load_dir + file_name)
        # First check if this is an old pickle version, if so transform it into a df
        if type(df) != pd.DataFrame:
            loaded_par = df
            df = pd.DataFrame(columns=['key', 'value'])
            for key, v in loaded_par.__dict__.items():
                try:
                    for key2, vv in v.__dict__.items():
                        temp = pd.DataFrame(data=[str(key) + '_' + str(key2), vv], index=['key', 'value']).T
                        df = df.append(temp)

                except:
                    temp = pd.DataFrame(data=[key, v], index=['key', 'value']).T
                    df = df.append(temp)

        no_old_version_bug = True

        for key, v in self.__dict__.items():
            try:
                for key2, vv in v.__dict__.items():
                    t = df.loc[df['key'] == str(key) + '_' + str(key2), 'value']
                    if t.shape[0] == 1:
                        tt = t.values[0]
                        self.__dict__[key].__dict__[key2] = tt
                    else:
                        if no_old_version_bug:
                            no_old_version_bug = False
                            print('#### Loaded parameters object is depreceated, default version will be used')
                        print('Parameter', str(key) + '.' + str(key2), 'not found, using default: ',
                              self.__dict__[key].__dict__[key2])

            except:
                t = df.loc[df['key'] == str(key), 'value']
                if t.shape[0] == 1:
                    tt = t.values[0]
                    self.__dict__[key] = tt
                else:
                    if no_old_version_bug:
                        no_old_version_bug = False
                        print('#### Loaded parameters object is depreceated, default version will be used')
                    print('Parameter', str(key), 'not found, using default: ', self.__dict__[key])


