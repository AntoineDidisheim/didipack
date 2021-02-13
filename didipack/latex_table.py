import pandas as pd
import numpy as np
import statsmodels.api as sm
from enum import Enum

class ParValue(Enum):
    TSTAT = 1
    PVALUE = 2
    STD = 3

class OneReg:
    def __init__(self, reg, show_list=[], hide_list=[], blocks=[], bottom_blocks=[]):
        self.reg = reg
        if show_list == []:
            self.show_list = []
            for s in self.reg.params.keys():
                if s not in hide_list:
                    self.show_list.append(s)
        else:
            self.show_list = show_list

        self.blocks = blocks
        self.bottom_block = bottom_blocks

    def create_columns(self):
        # first add the parameters of the reg
        d = pd.Series(dtype=object)
        for k in self.show_list:
            if k in self.reg.params.keys():
                v = self.reg.pvalues[k]
                p = f'{np.round(self.reg.params[k], TableReg.round):,}'
                for tr in TableReg.sign_tr:
                    if v <= tr:
                        p += '*'
                # self = table_2.reg_list[0]
                # update the v to be tstat or std depending on parameters
                if TableReg.par_value == ParValue.TSTAT:
                    v = self.reg.tvalues[k]
                if TableReg.par_value == ParValue.STD:
                    v = self.reg.bse[k]
                v = r'(' + f'{np.round(v, TableReg.round):,}' + r')'
                v_l = [len(x) for x in v.split('.')]
                p_l = [len(x) for x in p.split('.')]

                t = abs(v_l[0] - p_l[0])
                t = r'\phantom{' + '*' * t + '}'
                if v_l[0] > p_l[0]:
                    p = t + p
                if v_l[0] < p_l[0]:
                    v = t + v
                t = abs(v_l[1] - p_l[1])
                t = r'\phantom{' + '*' * t + '}'
                if v_l[1] > p_l[1]:
                    p = p+t
                if v_l[1] < p_l[1]:
                    v = v+t

                # else:
                    # p = r'\phantom{(}' + p + r'\phantom{)}'
                d[k] = p

                t = pd.Series(dtype=object)
                t[''] =v

                d = d.append(t)
            else:
                t = pd.Series(dtype=object)
                t[k] = TableReg.missing_symbol
                t[''] = TableReg.missing_symbol
                d = d.append(t)
        # now we can add the "blocks", that is fix effects and others
        for block in self.blocks:
            t = pd.Series(dtype=object)
            t[TableReg.group_key] = ''

            for k in block.keys():
                t[k] = block[k]
            d = d.append(t)

        # finaly additional info (r² and n.obs per default, but you can add anything through bottom blocks
        if TableReg.show_obs | TableReg.show_r2 | (len(self.bottom_block)>0):
            t = pd.Series(dtype=object)
            t[TableReg.group_key] = ''
            t['Observations'] = f'{int(self.reg.nobs):,}'

            if hasattr(self.reg,'rsquared_adj'):

                t[r'$R^2$'] = np.round(self.reg.rsquared_adj,TableReg.round_r2)
            else:
                t[r'Pseudo $R^2$'] = np.round(self.reg.prsquared,TableReg.round_r2)

            first_block = True
            for block in self.bottom_block:
                if first_block:
                    first_block = False
                else:
                    t[TableReg.group_key] = ''
                t = pd.Series(dtype=object)
                for k in block.keys():
                    t[k] = block[k]
            d = d.append(t)
        return d


class TableReg:
    missing_symbol = ' '
    par_value = ParValue.STD
    round = 4
    round_r2 = 4
    sign_tr = [0.1, 0.05, 0.01]
    show_obs = True
    show_r2 = True
    variable_skip = r'\smallskip'
    group_key = 'asgeg'
    group_skip = r'\medskip'
    equal_lines = False

    def __init__(self, **option):
        self.reg_list = []
        self.hide_list = []
        self.order = []
        self.df = None
        self.final_show_list = []
        self.show_only_list = []
        self.col_groups = []
        self.rename_dict = {}
        if 'hide_list' in option:
            assert type(option['hide_list']) == list, "The overall hide list has to be a list"
            self.hide_list = option['hide_list']

        if 'show_only_list' in option:
            assert type(option['show_only_list']) == list, "The show only  list has to be a list"
            self.show_only_list = option['show_only_list']

        if 'order' in option:
            assert type(option['order']) == list, "The order has to be a list"
            self.order = option['order']

        if 'col_groups' in option:
            self.set_col_groups(option['col_groups'])

        if 'rename_dict' in option:
            self.set_rename_dict(option['rename_dict'])


    def set_rename_dict(self, rename_dict):
        assert type(rename_dict) == dict, "The rename dict must be a dictionary"
        self.rename_dict = rename_dict



    def set_col_groups(self, groups):
        assert type(groups) == list, "The col order has to be a list of list"
        for group in groups:
            assert type(group) == list, "Each col group must be a list ['name of group', first columne in the group (int), last col in group (int)]"
        self.col_groups = groups


    def add_reg(self, reg, show_list=[], hide_list=[], blocks=[],bottom_blocks=[]):
        hide_list = hide_list + self.hide_list
        self.reg_list.append(OneReg(reg, show_list, hide_list, blocks, bottom_blocks))

    def update_show_list(self):
        if len(self.show_only_list) == 0:
            show_list = []
            for oneReg in self.reg_list:
                show_list = list(set(show_list + oneReg.show_list))
            show_list = list(np.sort(show_list))
            show_list = self.order + [x for x in show_list if x not in self.order]
        else:
            show_list = self.show_only_list

        col = []
        for oneReg in self.reg_list:
            oneReg.show_list = show_list
            col.append(oneReg.create_columns())
        self.df = pd.concat(col,1)

        self.df.columns = [r'\parboxc{c}{0.6cm}{('+str(int(i+1))+')}' for i in range(self.df.shape[1])]
        self.df = self.df.rename(index=self.rename_dict)

        self.final_show_list = show_list
        self.final_show_list = pd.Series(self.final_show_list).replace(self.rename_dict).values.tolist()
        self.tex=''

    def create_tex(self):
        self.update_show_list()

        # writing the tex modification to include name templatess
        tex = self.df.to_latex(escape=False)
        cols = tex.split('\\begin{tabular}{')[1].split('}')[0]
        rep = list(cols.replace('l','c'))
        rep[0] = 'l'
        tex = tex.replace(cols,''.join(rep))

        if len(self.col_groups)>0:
            # adding "group col names"
            s = '\n '
            s_line = '\n '
            for g in self.col_groups:
                s += '& \multicolumn{'+str(1+g[2]-g[1])+'}{c}{\parboxc{c}{0.6cm}{'+g[0]+'}}'
                # s += '& \multicolumn{'+str(1+g[2]-g[1])+'}{c}{'+g[0]+'}'
                s_line += r'\cmidrule(lr){'+str(g[1]+1)+'-'+str(g[2]+1)+'}'
            s += r' \\'+'\n'
            s_line += '\n'

            ts = tex.split(r'\toprule')
            tex = ts[0]+r'\toprule' + s +s_line+ ts[1]

            ts = tex.split(r'\midrule')
            tex = ts[0]+r'\midrule' + ts[1]

        # adding the skip between variable
        # first we extract the maxium length of a column on the first one
        L = 0
        for x in self.df.index:
            L = max(L,len(x))
        L+=1
        for i in range(1,len(self.final_show_list)):
            a = self.final_show_list[i]
            a += ' '*(L-len(a))+'&'
            ts = tex.split(a)
            temp = ts[0][:-4] + TableReg.variable_skip + ts[0][-4:]
            tex=temp+a+ts[1]


        # processing the group skip
        t = None
        for item in tex.split("\n"):
            if TableReg.group_key in item:
                t = item
        # replacing specific rule

        if t is not None:
            self.tex = tex.replace(t, TableReg.group_skip + r'\\')
        else:
            self.tex = tex

    def save_tex(self, save_dir):

        self.create_tex()
        tex = self.tex
        if TableReg.equal_lines:
            tex=tex.replace(r'\toprule',r'\hline')
            tex=tex.replace(r'\midrule',r'\hline')
            tex=tex.replace(r'\bottomrule',r'\hline')

        with open(save_dir,'w') as txt:
            txt.write(tex)

    @staticmethod
    def create_panel_of_tables(table_list, name_list, save_dir):
        numbers = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
        title_list = []
        for i in range(len(table_list)):
            table_list[i].create_tex()
            title_list.append('Panel '+numbers[i]+': '+name_list[i])


        tex = table_list[0].tex
        temp = r' \multicolumn{6}{c}{\parboxc{c}{0.7cm}{'+title_list[i]+r'}} \\'
        ts = tex.split(r'\toprule')
        tex = ts[0]+r'\toprule' +temp+r'\hline'+ts[1]
        tex = tex.replace(r'\bottomrule','')
        tex = tex.replace(r'\end{tabular}',r'asf')
        tex = tex.replace('\\\\\n\nasf','\\bigskip \\\\ \n')


        for i in range(1,len(table_list)):
            t_tex = table_list[i].tex
            temp = r' \multicolumn{6}{c}{\parboxc{c}{0.6cm}{' + title_list[i] + r'}} \\'
            ts = t_tex.split(r'\toprule')
            t_tex = ts[0] + r'\hline' + temp + r'\hline' + ts[1]
            t = None
            for item in t_tex.split("\n"):
                if r'\begin{tabular}' in item:
                    t = item
            t_tex = t_tex.replace(t,'')
            if i+1 < len(table_list):
                t_tex = t_tex.replace(r'\bottomrule','')
                t_tex = t_tex.replace(r'\end{tabular}', r'asf')
                t_tex = t_tex.replace('\\\\\n\nasf', '\\bigskip \\\\ \n')
            tex +=t_tex



        with open(save_dir,'w') as txt:
            txt.write(tex)



