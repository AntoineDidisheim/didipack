import pandas as pd
import numpy as np
import statsmodels.api as sm
from enum import Enum
import os
import didipack


class LatexPaper:

    def __init__(self, dir_, fig_type_default='.png'):
        if dir_[-1] != '/':
            dir_ += '/'
        self.dir = dir_
        self.dir_tables = dir_ + 'tables/'
        self.dir_figs = dir_ + 'figs/'
        self.dir_sec = dir_ + 'sec/'
        self.fig_type_default = fig_type_default

    def create_paper(self, tex_name, title="Paper Title", author="Firstname Name", sec=[]):
        tex_name = tex_name.replace('.tex','')
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if not os.path.exists(self.dir_sec):
            os.makedirs(self.dir_sec)
        if not os.path.exists(self.dir_figs):
            os.makedirs(self.dir_figs)
        if not os.path.exists(self.dir_tables):
            os.makedirs(self.dir_tables)

        with open(f'{self.dir}versionPO.sty', 'w') as txt:
            txt.write(didipack.TexRessources.versionPO_sty)

        if not os.path.exists(f'{self.dir_sec}abstract.tex'):
            with open(f'{self.dir_sec}abstract.tex', 'w') as txt:
                txt.write('')

        for r in sec:
            if not os.path.exists(f'{self.dir_sec + r}.tex'):
                with open(f'{self.dir_sec + r}.tex', 'w') as txt:
                    txt.write('')

        if not os.path.exists(f'{self.dir}/bib.bib'):
            with open(f'{self.dir}/sec/bib.bib', 'w') as txt:
                txt.write('')

        with open(f'{self.dir}jf.sty', 'w') as txt:
            txt.write(didipack.TexRessources.jf_sty)

        with open(f'{self.dir + tex_name}.tex', 'w') as txt:
            txt.write(didipack.TexRessources.m_tex_1 + title)
            txt.write(didipack.TexRessources.m_tex_2 + author)
            txt.write(didipack.TexRessources.m_tex_3)
            for r in sec:
                t = r"%%%%%%%%%%%%%%%%%%%%%%%%%" + '\n' \
                                                   r"\section{" + r + "}" + '\n' \
                                                                            r"\label{sec:" + r + "}" + '\n' \
                                                                                                       r"%%%%%%%%%%%%%%%%%%%%%%%%" + '\n' \
                                                                                                                                     r"\input{sec/" + r + ".tex}" + '\n' + '\n'

                txt.write(t)

            txt.write(didipack.TexRessources.m_tex_4 + "bib")
            txt.write(didipack.TexRessources.m_tex_5)

    def append_table_to_sec(self, table_name, sec_name, caption='caption',overall_caption=None,sub_dir=None, resize=-1):
        table_name = table_name.replace('.tex', '')
        sec_name = sec_name.replace('.tex', '')
        if overall_caption is None:
            overall_caption = table_name
        t0 = "\n"+ '\\begin{table}[H] \n \\centering \n \\caption{'
        t1 = '}\n\\label{table:'
        if resize > 0:
            t2 = f'}}\n \\resizebox{{{resize}\\textwidth}}{{!}}{{\\input{{tables/'
            t3 = '.tex}} \n\\end{table}'
        else:
            t2 = '}\n \\input{tables/'
            t3 = '.tex} \n\\end{table}' + '\n'

        if sub_dir is None:
            final_name = table_name
        else:
            final_name = sub_dir+'/'+table_name

        f = t0 + caption + t1 + overall_caption + t2 + final_name + t3

        with open(f'{self.dir_sec + sec_name}.tex', 'a') as txt:
            txt.write(f)

    fig_names = ['f1', 'f2.png'];
    sec_name = 'some_sec';
    main_caption = 'CAPTION';
    fig_labels = ['a', 'b'];
    fig_type_default = '.png'

    def append_fig_to_sec(self, fig_names, sec_name, main_caption='CAPTION', size=None, fig_captions=[], fig_type=None,overall_label=None, sub_dir = None):
        if fig_type is None:
            fig_type = self.fig_type_default

        if not type(fig_names) == list:
            fig_names = [fig_names]

        fig_names = [x.replace(fig_type, '') for x in fig_names]


        if overall_label is None:
            overall_label = fig_names[0]

        if size is None:
            # select default size
            if len(fig_names) == 1:
                size = "80mm"
            if len(fig_names) in [2, 4, 8]:
                size = r"0.45\linewidth"
            if len(fig_names) in [3, 6, 9]:
                size = r"0.3\linewidth"

        t1 = "\n"+r"\begin{figure}[t!] " + '\n' + "\centering"
        t2 = ''
        for i in range(len(fig_names)):
            let = "abcdefghijklmnopqrstuvwxyz"[i]

            if i < len(fig_captions):
                cap = fig_captions[i]
            else:
                cap = ''
            if sub_dir is None:
                name = fig_names[i]
            else:
                name = sub_dir +'/' + fig_names[i]

            t2 += r"\subfigure[" + cap + r"]{\label{fig:" + overall_label + "_" + let + r"}\includegraphics[width=" + size + r"]{figs/" + name + fig_type + r"}}" + '\n'
        t3 = r"\caption{" + main_caption + r"}" + '\n' +r"\label{fig:" + overall_label + r"}" +'\n'+ r"\end{figure}" + '\n'
        f = t1 + t2 + t3

        with open(f'{self.dir_sec + sec_name}.tex', 'a') as txt:
            txt.write(f)

    def append_text_to_sec(self, sec_name, text):
        txt = open(f'{self.dir_sec + sec_name}.tex','a')
        txt.write("\n"+text+"\n")
        txt.close()

    def create_new_sec(self, sec_name, text=""):
        with open(f'{self.dir_sec + sec_name}.tex', 'w') as txt:
            txt.write(text)


