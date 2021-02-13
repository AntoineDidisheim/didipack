import pandas as pd
import numpy as np
import statsmodels.api as sm
from enum import Enum
import os

class TexRessources:
    m_tex_1 = "% $Id: jfsample.tex,v 19:a118fd22993e 2013/05/24 04:57:55 stanton $" + "\n" + \
              "\documentclass[12pt]{article}" + "\n" + \
              r"" + "\n" + \
              r"% DEFAULT PACKAGE SETUP" + "\n" + \
              r"" + "\n" + \
              r"\usepackage{setspace,graphicx,epstopdf,amsmath,amsfonts,amssymb,amsthm,versionPO}" + "\n" + \
              r"\usepackage{marginnote,datetime,enumitem,subfigure,rotating,fancyvrb}" + "\n" + \
              r"%\usepackage{marginnote,datetime,enumitem,subfigure,fancyvrb}" + "\n" + \
              r"\usepackage{float}" + "\n" + \
              r"\usepackage[" + "\n" + \
              r"  colorlinks=true," + "\n" + \
              r"  linkcolor=blue," + "\n" + \
              r"  citecolor=blue]{hyperref}" + "\n" + \
              r"\usepackage{booktabs}" + "\n" + \
              r"\usepackage[longnamesfirst]{natbib}" + "\n" + \
              r"\usepackage{mathtools}" + "\n" + \
              r"\usepackage{lscape}" + "\n" + \
              r"\usepackage[toc,page]{appendix}" + "\n" + \
              r"% custom antoine stuff" + "\n" + \
              r"\def\rot{\rotatebox}" + "\n" + \
              r"\usepackage{tikz}" + "\n" + \
              r"\usetikzlibrary{positioning}" + "\n" + \
              r"\usepackage{forest}" + "\n" + \
              r"\newtheorem{prop}{Proposition}" + "\n" + \
              r"\usetikzlibrary{trees}" + "\n" + \
              r"" + "\n" + \
              r"\usdate" + "\n" + \
              r"" + "\n" + \
              r"% These next lines allow including or excluding different versions of text" + "\n" + \
              r"% using versionPO.sty" + "\n" + \
              r"" + "\n" + \
              r"\excludeversion{notes}        % Include notes?" + "\n" + \
              r"\includeversion{links}          % Turn hyperlinks on?" + "\n" + \
              r"" + "\n" + \
              r"% Turn off hyperlinking if links is excluded" + "\n" + \
              r"\iflinks{}{\hypersetup{draft=true}}" + "\n" + \
              r"" + "\n" + \
              r"% Notes options" + "\n" + \
              r"\ifnotes{%" + "\n" + \
              r"\usepackage[margin=1.0in,paperwidth=10in,right=2.5in]{geometry}%" + "\n" + \
              r"\usepackage[textwidth=1.4in,shadow,colorinlistoftodos]{todonotes}%" + "\n" + \
              r"}{%" + "\n" + \
              r"\usepackage[margin=1in]{geometry}%" + "\n" + \
              r"\usepackage[disable]{todonotes}%" + "\n" + \
              r"}" + "\n" + \
              r"" + "\n" + \
              r"\newlength\mytemplength" + "\n" + \
              r"\newcommand\parboxc[3]{%" + "\n" + \
              r"    \settowidth{\mytemplength}{#3}%" + "\n" + \
              r"    \parbox[#1][#2]{\mytemplength}{\centering #3}%" + "\n" + \
              r"}" + "\n" + \
              r"" + "\n" + \
              r"% make footnote pripritary so we don't split them from page to page" + "\n" + \
              r"\interfootnotelinepenalty=10000" + "\n" + \
              r"% Allow todonotes inside footnotes without blowing up LaTeX" + "\n" + \
              r"% Next command works but now notes can overlap. Instead, we'll define" + "\n" + \
              r"% a special footnote note command that performs this redefinition." + "\n" + \
              r"%\renewcommand{\marginpar}{\marginnote}%" + "\n" + \
              r"" + "\n" + \
              r"% Save original definition of \marginpar" + "\n" + \
              r"\let\oldmarginpar\marginpar" + "\n" + \
              r"" + "\n" + \
              r"% Workaround for todonotes problem with natbib (To Do list title comes out wrong)" + "\n" + \
              r"\makeatletter\let\chapter\@undefined\makeatother % Undefine \chapter for todonotes" + "\n" + \
              r"" + "\n" + \
              r"% Define note commands" + "\n" + \
              r"\newcommand{\smalltodo}[2][] {\todo[caption={#2}, size=\scriptsize, fancyline, #1] {\begin{spacing}{0.5}#2\end{spacing}}}" + "\n" + \
              r"\newcommand{\rhs}[2][]{\smalltodo[color=green!30,#1]{{\bf RS:} #2}}" + "\n" + \
              r"\newcommand{\rhsnolist}[2][]{\smalltodo[nolist,color=green!30,#1]{{\bf RS:} #2}}" + "\n" + \
              r"\newcommand{\rhsfn}[2][]{%  To be used in footnotes (and in floats)" + "\n" + \
              r"\renewcommand{\marginpar}{\marginnote}%" + "\n" + \
              r"\smalltodo[color=green!30,#1]{{\bf RS:} #2}%" + "\n" + \
              r"\renewcommand{\marginpar}{\oldmarginpar}}" + "\n" + \
              r"%\newcommand{\textnote}[1]{\ifnotes{{\noindent\color{red}#1}}{}}∫" + "\n" + \
              r"\newcommand{\textnote}[1]{\ifnotes{{\colorbox{yellow}{{\color{red}#1}}}}{}}" + "\n" + \
              r"\newcommand{\fixmeAntoine}[1]{\textcolor{red}{\textbf{TBD Antoine: #1}}}" + "\n" + \
              r"\newcommand{\fixmeHui}[1]{\textcolor{blue}{\textbf{TBD Hui: #1}}}" + "\n" + \
              r"\newcommand{\fixmeSimon}[1]{\textcolor{purple}{\textbf{TBD Simon: #1}}}" + "\n" + \
              r"\newcommand{\alll}[1]{\textcolor{teal}{\textbf{TBD All: #1}}}" + "\n" + \
              r"" + "\n" + \
              r"% \input{tex/commands.tex}" + "\n" + \
              r"" + "\n" + \
              r"% Command to start a new page, starting on odd-numbered page if twoside option" + "\n" + \
              r"% is selected above" + "\n" + \
              r"\newcommand{\clearRHS}{\clearpage\thispagestyle{empty}\cleardoublepage\thispagestyle{plain}}" + "\n" + \
              r"" + "\n" + \
              r"% Number paragraphs and subparagraphs and include them in TOC" + "\n" + \
              r"\setcounter{tocdepth}{2}" + "\n" + \
              r"\usepackage{bbm}" + "\n" + \
              r"% JF-specific includes:" + "\n" + \
              r"" + "\n" + \
              r"\usepackage{indentfirst} % Indent first sentence of a new section." + "\n" + \
              r"%\usepackage{endnotes}    % Use endnotes instead of footnotes" + "\n" + \
              r"\usepackage{jf}          % JF-specific formatting of sections, etc." + "\n" + \
              r"\usepackage[labelfont=bf,labelsep=period]{caption}   % Format figure captions" + "\n" + \
              r"\captionsetup[table]{labelsep=none}" + "\n" + \
              r"" + "\n" + \
              r"% Define theorem-like commands and a few random function names." + "\n" + \
              r"\newtheorem{condition}{CONDITION}" + "\n" + \
              r"\newtheorem{corollary}{COROLLARY}" + "\n" + \
              r"\newtheorem{proposition}{PROPOSITION}" + "\n" + \
              r"\newtheorem{obs}{OBSERVATION}" + "\n" + \
              r"\newcommand{\argmax}{\mathop{\rm arg\,max}}" + "\n" + \
              r"\newcommand{\defeq}{\stackrel{\rm def}{=}}" + "\n" + \
              r"\def\QQ{{\mathbb Q}}" + "\n" + \
              r"" + "\n" + \
              r"\usepackage{caption}" + "\n" + \
              r"" + "\n" + \
              r"" + "\n" + \
              r"\captionsetup[table]{" + "\n" + \
              r"  labelsep=newline," + "\n" + \
              r"  justification=centerfirst" + "\n" + \
              r"}" + "\n" + \
              r"" + "\n" + \
              r"\usepackage{changes}" + "\n" + \
              r"\definechangesauthor[name={HC}, color=red]{HC}" + "\n" + \
              r"" + "\n" + \
              r"" + "\n" + \
              r"" + "\n" + \
              r"\begin{document}" + "\n" + \
              r"" + "\n" + \
              r"\setlist{noitemsep}  % Reduce space between list items (itemize, enumerate, etc.)" + "\n" + \
              r"\onehalfspacing      % Use 1.5 spacing" + "\n" + \
              r"%\doublespacing      % Use 2.0 spacing" + "\n" + \
              r"\parskip 3pt" + "\n" + \
              r"" + "\n" + \
              r"" + "\n" + \
              r"" + "\n" + \
              r"\title{" + "\n"

    m_tex_2 = "}\n \\author{"

    m_tex_3 = "}" + "\n" + \
              r"" + "\n" + \
              r"\date{\today}" + "\n" + \
              r"" + "\n" + \
              r"% Create title page with no page number" + "\n" + \
              r"" + "\n" + \
              r"\maketitle" + "\n" + \
              r"\thispagestyle{empty}" + "\n" + \
              r"" + "\n" + \
              r"\bigskip" + "\n" + \
              r"" + "\n" + \
              r"\begin{abstract}" + "\n" + \
              r"\input{sec/abstract.tex}" + "\n" + \
              r"\end{abstract}" + "\n" + \
              r"" + "\n" + \
              r"\medskip" + "\n" + \
              r"" + "\n" + \
              r"%\begin{centering}" + "\n" + \
              r"%{\large{\textbf{This is a preliminary draft. Please do not cite or distribute without permission" + "\n" + \
              r"%of the authors.}}}\\" + "\n" + \
              r"%\end{centering}" + "\n" + \
              r"" + "\n" + \
              r"\clearpage" + "\n" + \
              r"" + "\n" + \
              r"\setcounter{page}{1}"
    m_tex_4 = r"% Bibliography." + "\n" + \
              "\n" + \
              r"\begin{onehalfspacing}   % Double-space the bibliography" + "\n" + \
              r"\bibliographystyle{jf}" + "\n" + \
              r"\bibliography{"
    m_tex_5 = r"}" + "\n" + \
              r"\end{onehalfspacing}" + "\n" + \
              r"\end{document}"

    versionPO_sty = r"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" + "\n" + \
                    r"% You need Rainer Schoepf's verbatim.sty to use this!!" + "\n" + \
                    r"%" + "\n" + \
                    r"% Version control macros. These let you define environments whose contents" + "\n" + \
                    r"% will be optionally added to or deleted from the text when you run LaTeX." + "\n" + \
                    r"% Usage: place either of the following near the start of your file:" + "\n" + \
                    r"%     \includeversion{NAME}" + "\n" + \
                    r"%     \excludeversion{NAME}" + "\n" + \
                    r"% Here, NAME is any name you choose. The first one indicates that text" + "\n" + \
                    r"% between \begin{NAME} and \end{NAME} will be processed in the normal way." + "\n" + \
                    r"% The second indicates that text between \begin{NAME} and \end{NAME} will" + "\n" + \
                    r"% be totally deleted." + "\n" + \
                    r"% These command automatically declare the inverted version not-NAME." + "\n" + \
                    r"%" + "\n" + \
                    r"% NOTE:" + "\n" + \
                    r"% You cannot use the version environments inside another environment," + "\n" + \
                    r"% inside a command or in an argument to another command. You can make a" + "\n" + \
                    r"% limited use of a version inside an environment by using \NAME and" + "\n" + \
                    r"% \endNAME rather than \begin{NAME} and \end{NAME}. E.g." + "\n" + \
                    r"%   \newenvironment{example}{...\myversion...}{\endmyversion} where the" + "\n" + \
                    r"% following would fail:" + "\n" + \
                    r"%   \newenvironment{example}{...\begin{myversion}...}{\end{myversion}}" + "\n" + \
                    r"%" + "\n" + \
                    r"% To alleviate these problems a bit, foreach version NAME also a command" + "\n" + \
                    r"% \ifNAME is defined such that \ifNAME{yes-part}{no-part} selects either" + "\n" + \
                    r"% yes-part or no-part depending on whether the version is included or" + "\n" + \
                    r"% excluded. The \ifNAME command may be used everywhere but the environments" + "\n" + \
                    r"% are preferred with large amounts of text. Also the parameters of \ifNAME" + "\n" + \
                    r"% are not included in a group, so you can make global declarations in them." + "\n" + \
                    r"% The \ifNAME command is fragile if either of its arguments is fragile." + "\n" + \
                    r"% Note: the \ifNAME command is only usable if NAME consists of letters only." + "\n" + \
                    r"%" + "\n" + \
                    r"% A ``comment'' environment has already been pre-defined for you with " + "\n" + \
                    r"% \excludeversion{comment}; you can NOT override this one." + "\n" + \
                    r"%" + "\n" + \
                    r"% You can define environments for as many versions as you want. " + "\n" + \
                    r"%" + "\n" + \
                    r"% Example: " + "\n" + \
                    r"%   \includeversion{abridged}" + "\n" + \
                    r"%   \ifabridged{\large}{\small}" + "\n" + \
                    r"%   Text for the" + "\n" + \
                    r"%   \begin{abridged} " + "\n" + \
                    r"%      short" + "\n" + \
                    r"%   \end{abridged}" + "\n" + \
                    r"%   \begin{not-abridged}" + "\n" + \
                    r"%      long and really longwinded, opaque and boring" + "\n" + \
                    r"%   \end{not-abridged}" + "\n" + \
                    r"%   version of the paper. Punctuation works correctly\begin{not-abridged}" + "\n" + \
                    r"%   because sphack is used\end{not-abridged}." + "\n" + \
                    r"%   \begin{comment} This is deleted by default. \end{comment}" + "\n" + \
                    r"%" + "\n" + \
                    r"%  Piet van Oostrum -- <piet@cs.ruu.nl>" + "\n" + \
                    r"%  Idea based on a style file by Stephen Bellantoni, implementation based" + "\n" + \
                    r"%  on verbatim.sty by Rainer Schoepf <SCHOEPF@SC.ZIB-Berlin.DE>." + "\n" + \
                    r"" + "\n" + \
                    r"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" + "\n" + \
                    r"" + "\n" + \
                    r"\@ifundefined{verbatim@@@}{\input{verbatim.sty}}{}" + "\n" + \
                    r"" + "\n" + \
                    r"\def\includeversion#1{%" + "\n" + \
                    r"  \expandafter\def\csname #1\endcsname{}%" + "\n" + \
                    r"  \expandafter\def\csname end#1\endcsname{}%" + "\n" + \
                    r"  \expandafter\let\csname not-#1\endcsname\comment" + "\n" + \
                    r"  \expandafter\let\csname endnot-#1\endcsname\endcomment" + "\n" + \
                    r"  \expandafter\def\csname if#1\endcsname##1##2{##1}" + "\n" + \
                    r"}" + "\n" + \
                    r"\def\excludeversion#1{%" + "\n" + \
                    r"  \expandafter\let\csname #1\endcsname\comment" + "\n" + \
                    r"  \expandafter\let\csname end#1\endcsname\endcomment" + "\n" + \
                    r"  \expandafter\def\csname not-#1\endcsname{}%" + "\n" + \
                    r"  \expandafter\def\csname endnot-#1\endcsname{}%" + "\n" + \
                    r"  \expandafter\def\csname if#1\endcsname##1##2{##2}" + "\n" + \
                    r"}"

    jf_sty = "% Formatting for Journal of Finance papers" + "\n" + \
             r"% Theorems, etc. (need to load amsthm first)" + "\n" + \
             r"\newtheoremstyle{jf}% name" + "\n" + \
             r"{6pt}% Space above" + "\n" + \
             r"{6pt}% Space below" + "\n" + \
             r"{\itshape}% Body font" + "\n" + \
             r"{}% Indent amount" + "\n" + \
             r"{}% Theorem head font" + "\n" + \
             r"{:}% Punctuation after theorem head" + "\n" + \
             r"{.5em}% Space after theorem head" + "\n" + \
             r"{}% Theorem head spec (can be left empty, meaning normal)" + "\n" + \
             r"" + "\n" + \
             r"\theoremstyle{jf}" + "\n" + \
             r"" + "\n" + \
             r"% Make References title all caps." + "\n" + \
             r"\renewcommand{\refname}{REFERENCES}" + "\n" + \
             r"" + "\n" + \
             r"% Put dots after numbers in section headers." + "\n" + \
             r"\renewcommand{\@seccntformat}[1]{{\csname the#1\endcsname}.\hspace{1em}}" + "\n" + \
             r"" + "\n" + \
             r"% Section and table numbers " + "\n" + \
             r"\def\thesection       {\Roman{section}}" + "\n" + \
             r"\def\thesubsection    {\Alph{subsection}}" + "\n" + \
             r"\def\thetable         {\Roman{table}}" + "\n" + \
             r"" + "\n" + \
             r"% Section header format" + "\n" + \
             r"\renewcommand{\section}{\@startsection" + "\n" + \
             r"  {section}{1}{0mm}{-3.5ex \@plus -1ex \@minus -.2ex}{2.3ex \@plus.2ex}{\centering\normalfont\Large\bfseries}}" + "\n" + \
             r"" + "\n" + \
             r"\renewcommand{\subsection}{\@startsection" + "\n" + \
             r"  {subsection}{2}{0mm}{-3.25ex \@plus -1ex \@minus -.2ex}{1.5ex \@plus.2ex}{\normalfont\large\itshape}}" + "\n" + \
             r"" + "\n" + \
             r"% Put section number back in references to subsections and subsubsections." + "\n" + \
             r"\renewcommand{\p@subsection}{\thesection .}" + "\n" + \
             r"\renewcommand{\p@subsubsection}{\thesection .}" + "\n" + \
             r"" + "\n" + \
             r"% Appendix formatting:" + "\n" + \
             r"" + "\n" + \
             r"\def\appendix{\par" + "\n" + \
             r"  \setcounter{section}{0}%         % Start counting sections again" + "\n" + \
             r"  \setcounter{subsection}{0}% " + "\n" + \
             r"% Use uppercase letters for section numbers:" + "\n" + \
             r"  \gdef\thesection{\@Alph\c@section}% " + "\n" + \
             r"% Number equations (A1), etc.:" + "\n" + \
             r"  \renewcommand{\theequation}{\thesection\arabic{equation}}% " + "\n" + \
             r'% Put word "Appendix" before appendix number:' + "\n" + \
             r"  \renewcommand{\@seccntformat}[1]{{Appendix \csname the##1\endcsname}.\hspace{1em}}" + "\n" + \
             r"% Same formatting as above, but reset equation counter with each section" + "\n" + \
             r"  \renewcommand{\section}{\setcounter{equation}{0}\@startsection" + "\n" + \
             r"    {section}{1}{0mm}{-3.5ex \@plus -1ex \@minus -.2ex}{2.3ex \@plus.2ex}{\centering\normalfont\Large\bfseries}}" + "\n" + \
             r"}" + "\n" + \
             r"" + "\n"
