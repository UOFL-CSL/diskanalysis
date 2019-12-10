% uofl.cls: LaTeX class for University of Louisville MSc/MEng/PhD theses.
% $Id: uofl.cls,v 1.25 1997/09/12 01:24:31 tjchol01 Exp $
% Copyright 1996, 1997 by Tomasz J. Cholewo (t.cholewo@ieee.org)
%
% To do: no TOC in TOC, page numbering?
%
% -------------------------------------------------------------------------
% The up-to-date version of this file can be usually found at:
%
%    http://mecca.spd.louisville.edu/~tjchol01
%
% An example of suggested use is in the accompanying file uofl-example.tex.
%
% Only the MSc and MEng variants were used so far for successful theses.
% The MEng part may no longer be compliant.
%
% Please let me know of any remarks school authorities had about this style
% and about all interesting modifications you introduced so I can
% incorporate them in the next version. If you change this
% file in any way please rename it and clearly mark the changes, so as not
% to confuse other potential users.  All forms of appreciation from people
% who actually graduated using this class file are welcome :-).
% -------------------------------------------------------------------------
% Permission to use, copy, modify, and distribute this software and its
% documentation for any purpose and without fee is hereby granted,
% provided that the above copyright notice appear in all copies and that
% both that the copyright notice and this permission notice and warranty
% disclaimer appear in supporting documentation.  Tomasz J. Cholewo
% disclaims all warranties with regard to this software, including all
% implied warranties of merchantability and fitness.  In no event shall
% Tomasz J. Cholewo be liable for any special, indirect or consequential
% damages or any damages whatsoever resulting from loss of use, data or
% profits, whether in an action of contract, negligence or other tortious
% action, arising out of or in connection with the use or performance of
% this software.
%
% NO PERMISSION is granted to distribute a modified version of this file
% under its original name.
% -------------------------------------------------------------------------
% Identification:
% The code below is explained in the implementation
% documentation of the rcs package.
\begingroup
\def\RCSClass#1#2 $#3: #4 #5\endRCS $#6: #7 #8\endRCS{%
  \def\date{#4}\def\id{v#7}%
  \ProvidesClass{#1}[\date\space\id\space #2]%
  }

\RCSClass{uofl}{LaTeX markup for UofL MSc/MEng/PhD theses}
$Date: 1997/09/12 01:24:31 $\endRCS
$Revision: 1.25 $\endRCS
\endgroup

\NeedsTeXFormat{LaTeX2e}[1994/12/01]

% Options:
\newif\if@uofl@proposal@
\@uofl@proposal@false

% What degree do we wish to get
\DeclareOption{MSc}{%
  \gdef\@target{%
                               A Thesis\\
                   Submitted to the Faculty of the\\
           Graduate School of the University of Louisville\\
              in Partial Fulfillment of the Requirements\\
                            for the Degree of\\
                               \vskip 5em
                          Master of Science}%
  \gdef\@dissthes{Thesis}%
}

\DeclareOption{MEng}{%
  \gdef\@target{%
                               A Thesis\\
                   Submitted to the Faculty of the\\
                       University of Louisville\\
                       Speed Scientific School\\
              as Partial Fulfillment of the Requirements\\
                     for the Professional Degree of\\
                               \vskip 5em
                        MASTER OF ENGINEERING}%
  \gdef\@dissthes{Project}%
}

\DeclareOption{PhD}{%
  \gdef\@target{%
                           A Dissertation\\
                   Submitted to the Faculty of the\\
           Graduate School of the University of Louisville\\
              in Partial Fulfillment of the Requirements\\
                            for the Degree of\\
                               \vskip 5em
                         Doctor of Philosophy}%
  \gdef\@dissthes{Dissertation}%
}

\DeclareOption{PhDproposal}{%
  \gdef\@target{%
                        Dissertation Proposal\\
                            for the Degree of\\
                               \vskip 5em
                         Doctor of Philosophy}
  \gdef\@dissthes{Dissertation}%
  \@uofl@proposal@true%
}

% department
\DeclareOption{EE}{\gdef\@department{Department of Electrical Engineering}}
\DeclareOption{CSE}{\gdef\@department{Computer Science and Engineering
    Program\\University of Louisville}}
\DeclareOption{EMACS}{\gdef\@department{Department of Engineering
    Mathematics and Computer Science}}

\DeclareOption*{\typeout{Ignored unknown option \CurrentOption.}}
% not compatible with
\ExecuteOptions{MSc,EE}

\ProcessOptions

\def\UofLBaseClass{report}
\if@uofl@proposal@
  \PassOptionsToClass{10pt}{\UofLBaseClass}
\else
  \PassOptionsToClass{12pt}{\UofLBaseClass}
\fi
\LoadClass{\UofLBaseClass}
% -------------------------------------------------------------------------
% Title page:

\newcommand*{\target}[1]{\gdef\@target{#1}}     % allow \par
\newcommand{\department}[1]{\gdef\@department{#1}}
\newcommand{\degree}[1]{\gdef\@degree{#1}}
\newcommand{\committee}[1]{\gdef\@committee{#1}}

\newenvironment{@signed}%
  {\begin{tabular}[t]{p{40ex}}\hrulefill\\\centering}%
  {\end{tabular}}


\renewcommand\maketitle{%
\thispagestyle{empty}%
{%
  \null\vfil
  \vskip 60\p@
  \begin{center}%
                               \@title\\
                              \vskip 6em%
                                   By
                              \vskip 1em%
                               \@author\\
                               \@degree\\
                              \vskip 5em%
                               \@target\\
                               \vskip 5em
                              \@department\\
                               \vskip 3em
                                 \@date
  \end{center}
  \vfil\null
}%
%
\null
\if@uofl@proposal@
\else
{\newpage%
% empty page
%\thispagestyle{empty}%
%\null\newpage%
%
%% Damon does it this way (?)
\setcounter{page}{1}%
%\setcounter{page}{2}%
%
%
% Approval page:
{%
  \null\vfil
  \vskip 60\p@
  \begin{center}%
                               \@title\\
                              \vskip 3em%
                             Submitted by\\
                              \vskip 1em%
                               \@author\\
                              \vskip 3em%
                         A \@dissthes{} Approved on\\
                              \vskip 3em%
                  \begin{@signed}(Date)\end{@signed}\\
                              \vskip 4em%
         by the Following Reading and Examination Committee:\\
                               \vskip 3em
             {\def\and{\end{@signed}\\\\\\\begin{@signed}}%
                         \begin{tabular}[t]{c}%
                \begin{@signed}\@committee\end{@signed}%
                          \end{tabular}\par}%
  \end{center}
  \vfil\null%
%  \addcontentsline{toc}{chapter}{APPROVAL PAGE}%
}%
%\newpage
%
}\fi
\let\maketitle\relax
\gdef\@target{}%
\gdef\@thanks{}%
\gdef\@author{}\gdef\@title{}\gdef\@degree{}\gdef\@committee{}%
\doublespace
}

% used to avoid putting toc entries for preliminaries
\newif\if@mainmatter \@mainmatterfalse

\def\maybenonumber{} % front matter ``chapters'' have page numbers

\def\blockofcontents{%
  \tableofcontents
  \if@uofl@proposal@
  \else
    \listoftables
    \listoffigures
  \fi
  \newpage % to assure chapter 1 starts with page 1

  \@mainmattertrue
  \pagestyle{myheadings}%
  \pagenumbering{arabic}%
  \gdef\maybenonumber{\thispagestyle{empty}}% no body chapter page numbers
  \addtocontents{toc}{\protect\numberline{\chaptername}}%
}


% switch between single and double spacing
\newcommand{\singlespace}{\renewcommand{\baselinestretch}{1}\normalsize\relax}
\newcommand{\doublespace}{\renewcommand{\baselinestretch}{1.66}\normalsize\relax}
%\newcommand{\singlespace}{\linespread{1}}
%\newcommand{\doublespace}{\linespread{1.66}}

% disable hyphenation (sometimes useful in titles and captions)
\newcommand{\nohyphens}{\hyphenpenalty=10000\exhyphenpenalty=10000\relax}


% The following use \chapter* internally:
\renewcommand{\contentsname}{TABLE OF CONTENTS}
\renewcommand{\listtablename}{LIST OF TABLES}
\renewcommand{\listfigurename}{LIST OF FIGURES}
\renewcommand{\bibname}{REFERENCES}

\renewcommand{\chaptername}{CHAPTER}
\renewcommand{\appendixname}{APPENDIX}

% counters
\addtocounter{secnumdepth}{1}                   % show \subsubsection numbers
\addtocounter{tocdepth}{1}                      % also in TOC

% We have to be inconsistent with all these dots to follow requirements

\renewcommand{\thechapter}{\Roman{chapter}}     % no dot!
\renewcommand{\thesection}{\Alph{section}.}
\renewcommand{\thesubsection}{\arabic{subsection}.}
\renewcommand{\thesubsubsection}{\alph{subsubsection}.}

\renewcommand{\theequation}{\arabic{equation}}
\renewcommand{\thefigure}{\arabic{figure}}

% Damon
\renewcommand{\thetable}{\arabic{table}}
%\renewcommand{\thetable}{\Roman{table}}

% chapter should reset section, not figure or table counters
\def\cl@chapter{\@elt{section}}

% \ref should give multilevel references for sections.
% We use special \refthe commands for that purpose.
\newcommand{\refthechapter}{\Roman{chapter}}
\newcommand{\refthesection}{\refthechapter.\Alph{section}}
\newcommand{\refthesubsection}{\refthesection.\arabic{subsection}}
\newcommand{\refthesubsubsection}{\refthesubsection.\alph{subsubsection}}

\newcommand{\reftheequation}{\arabic{equation}}
\newcommand{\refthefigure}{\arabic{figure}}

% Damon
\newcommand{\refthetable}{\arabic{table}}
%\newcommand{\refthetable}{\Roman{table}}

\def\refstepcounter#1{\stepcounter{#1}%
  \protected@edef\@currentlabel
       {\csname p@#1\endcsname\csname refthe#1\endcsname}%
}

% TOC/LOT/LOF line spacings
\renewcommand*\l@chapter{\@dottedtocline{0}{0.0em}{3.3em}}
\renewcommand*\l@section{\@dottedtocline{1}{3.3em}{2.2em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{6.4em}{1.5em}}
\renewcommand*\l@subsubsection{\@dottedtocline{3}{7.9em}{1.5em}}

\renewcommand*\l@figure{\@dottedtocline{0}{0em}{6em}}
\renewcommand*\l@table{\@dottedtocline{0}{0em}{6em}}



% chapter headings
\renewcommand\chapter{\if@openright\cleardoublepage\else\clearpage\fi
                    \maybenonumber
                    \global\@topnum\z@
                    \@afterindentfalse
                    \secdef\@chapter\@schapter}

\def\@chapter[#1]#2{
  \if@mainmatter
    \ifnum \c@secnumdepth >\m@ne
    \refstepcounter{chapter}%
    \message{\@chapapp\space\roman{chapter}.}%
      \addcontentsline{toc}{chapter}% dot here!!!
      {\protect\numberline{\hfill\thechapter.\quad}%
% {\def\protect\baselinestretch{1}\baselineskip 0pt\lineskip 0pt\lineskiplimit 0pt #1}}%
       {\protect\singlespace #1}}%
     \else
       \addcontentsline{toc}{chapter}{\protect\singlespace{}#1}%
     \fi
   \fi
%    After having written an entry to the table of contents we store
%    the (alternative) title of this chapter with |\chaptermark| and
%    add some white space to the lists of figures and tables.
                    \chaptermark{#1}%
%%                    \addtocontents{lof}{\protect\addvspace{10\p@}}%
%%                    \addtocontents{lot}{\protect\addvspace{10\p@}}%
%    Then we call upon |\@makechapterhead| to format the actual
%    chapter title. We have to do this in a special way when we are in
%    twocolumn mode in order to have the chapter title use the entire
%    |\textwidth|. In one column mode we call |\@afterheading| which
%    takes care of suppressing the indentation.
                    \if@twocolumn
                      \@topnewpage[\@makechapterhead{#2}]%
                    \else
                      \@makechapterhead{#2}%
                      \@afterheading
                    \fi}


\renewcommand{\@makechapterhead}[1]{%
  \vspace*{50pt}%
  {\parindent \z@ \raggedright \normalfont\bfseries
    \interlinepenalty\@M
    {\singlespace\centering
     \@chapapp\space \thechapter
     \par\nobreak
     \vskip 5\p@
     \interlinepenalty\@M
     \textsc{#1}\par
    }%
    \nobreak
    \vskip 20\p@
  }}

\renewcommand{\@makeschapterhead}[1]{% starred
  \vspace*{50pt}%
  {\parindent \z@ \raggedright \normalfont\bfseries
    \interlinepenalty\@M
    \if@mainmatter
      \addcontentsline{toc}{chapter}{#1}%
    \fi
    {\singlespace\centering
     \interlinepenalty\@M
     #1\par}%
    \nobreak
    \vskip 20\p@
    }}

% section headings
\renewcommand{\section}{\par\vspace{1.5\baselineskip}\secdef\sectiona\sectionb}
\newcommand{\sectiona}[2][?]{%
  \refstepcounter{section}%
  \addcontentsline{toc}{section}{\protect\singlespace\protect\numberline{\hfill\thesection\quad}#1}%
  {\singlespace\normalfont\bfseries\nohyphens\centering\thesection\quad#2\par}%
\vspace{0.3\baselineskip}%
%\noindent
}

\newcommand{\sectionb}[1]{%
  \addcontentsline{toc}{section}{\protect\singlespace\numberline{}#1}%
  {\singlespace\normalfont\bfseries\nohyphens\centering#1\par}%
\vspace{0.3\baselineskip}%
%\noindent
}

\renewcommand{\subsection}{\@startsection{subsection}{2}{0ex}%
  {-\baselineskip}{0.5\baselineskip}{\normalfont\normalsize}}

\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{8ex}%
  {-0mm}{-2ex}{\normalfont\normalsize\itshape}}

\renewcommand\appendix{\par
  \setcounter{chapter}{0}%
  \setcounter{section}{0}%
  \renewcommand\@chapapp{\appendixname}%
  \renewcommand\thechapter{\Roman{chapter}}%
  \addtocontents{toc}{\protect\numberline{\appendixname}}%
}



% captions
\renewcommand{\figurename}{FIGURE}
\renewcommand{\tablename}{TABLE}

% We will have half of classes.dtx pretty soon in here :-)
\long\def\@caption#1[#2]#3{\par
  \addcontentsline{\csname ext@#1\endcsname}{#1}{%
    \protect\numberline{{\csname#1name\endcsname}\space
      \csname the#1\endcsname.}{\ignorespaces #2}}%
  \begingroup
  \@parboxrestore
  \normalsize
  \@makecaption{\csname fnum@#1\endcsname}{\ignorespaces #3}\par
  \endgroup
}

% FIGURE captions

\long\def\@makefigcaption#1#2{%
  \vskip\abovecaptionskip
%    We want to see if the caption fits on one line on the page,
%    therefore we first typeset it in a temporary box.
  \sbox\@tempboxa{\singlespace #1\,--\,#2}%
%    We can the measure its width. It that is larger than the current
%    |\hsize| we typeset the caption as an ordinary paragraph.
%    \begin{macrocode}
  \ifdim \wd\@tempboxa >\hsize
    \singlespace #1\,--\,#2\par
%    If the caption fits, we center it. Because this uses an |\hbox|
%    directly in vertical mode, it does not execute the |\everypar|
%    tokens; the only thing that could be needed here is resetting the
%    `minipage flag' so we do this explicitly.
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}

%\newcommand{\@makefigcaption}[2]{{\singlespace #1\,--\,#2\par}}
\renewcommand{\figure}{\let\@makecaption\@makefigcaption\@float{figure}\centering}

% TABLE captions

\long\def\@maketabcaption#1#2{%
  \vskip\abovecaptionskip
  \hb@xt@\hsize{\hfil#1\hfil}%
  \vskip 3mm%
%    We want to see if the caption fits on one line on the page,
%    therefore we first typeset it in a temporary box.
  \sbox\@tempboxa{\singlespace #2}%
%    We can the measure its width. It that is larger than the current
%    |\hsize| we typeset the caption as an ordinary paragraph.
%    \begin{macrocode}
  \ifdim \wd\@tempboxa >\hsize
    \singlespace #2\par
%    If the caption fits, we center it. Because this uses an |\hbox|
%    directly in vertical mode, it does not execute the |\everypar|
%    tokens; the only thing that could be needed here is resetting the
%    `minipage flag' so we do this explicitly.
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip 5mm}

%%\newcommand{\@maketabcaption}[2]{{\singlespace\centering#1\par\vspace*{3mm}%
%%% \MakeUppercase
%%  {#2}%
%%  \par\vspace*{5mm}}}
\renewcommand{\table}{\let\@makecaption\@maketabcaption\@float{table}\centering}

% margins
\oddsidemargin 0.5in
\evensidemargin 0.5in
\topmargin -0.5in
\textwidth 6in

% Damon (?)
\textheight 9in
\footskip .5in
%\textheight 8.5in
%\footskip .75in

\marginparsep 0in
\marginparwidth 0in

\headheight 12pt
\headsep 24.17pt  % text starts 1in from the top

% always do paragraph indent
\setlength\parindent{3em}
\let\@afterindentfalse\@afterindenttrue
\@afterindenttrue

% specific environments
\newenvironment{uenumerate}{\begin{enumerate}\setlength{\itemsep}{0pt}}{\end{enumerate}}
\newenvironment{uquotation}{\begin{quotation}\singlespace}{\end{quotation}}

% start in these page styles for the front matter
\pagestyle{plain}
\pagenumbering{roman}

% set the style for included CWEB programs
\def\cwebproghook{\singlespace\small\let\footnotesize=\scriptsize}

% That's all for today.
\endinput

% -------------------------------------------------------------------------
% $Log: uofl.cls,v $
% Revision 1.25  1997/09/12 01:24:31  tjchol01
% For Dave.
%
% Revision 1.24  1997/09/02 20:16:12  tjchol01
% Damon corrections.  Removed LOT and LOF from proposal.
%
% Revision 1.23  1997/07/22 16:28:26  tjchol01
% Changed thesis to dissertation for PhD, no uppercase for table captions,
% no dots after chapter numbers in the main body.
%
% Revision 1.22  1997/05/14 16:10:27  tjchol01
% \label now generates multilevel references.
%
% Revision 1.21  1997/04/16 02:55:09  tjchol01
% Front matter "chapters" have page numbers.
%
% Revision 1.20  1997/04/10 02:55:01  tjchol01
% Changed one title line in PhDproposal.
%
% Revision 1.19  1997/04/03 00:54:34  tjchol01
% Changed title page for PhDproposal.  New option CSE.
%
% Revision 1.18  1997/02/24 20:25:01  tjchol01
% Conditionals for PhDproposal.  Bold chapters.
%
% Revision 1.17  1997/02/21 05:23:55  tjchol01
% Corrected appendix numbers to Roman, chapter TOC \quad, singlespaced sections.
% Still doublespace in TOC/LOF/LOT.
%
% Revision 1.16  1997/02/17 00:47:13  tjchol01
% Appendix handling.  New PhDproposal option.  Added RCS identification.
% Chapter |\vspace*| corrected.  Page numbers in headings.  Table number
% and title separated with space.  Support for |\cwebproghook|.
% |\doublespace| moved to |\maketitle|.  Log moved to the end.
%
% Revision 1.15  1996/12/03 15:02:24  tjchol01
% Cover page improved:  long \target options and a new \department option.
%
% Revision 1.14  1996/11/25 03:35:55  tjchol01
% Legalese added.
%
% Revision 1.13  1996/11/25 02:35:15  tjchol01
% Corrected TOC, LOT and LOF spacings.
%
% Revision 1.12  1996/11/25 00:20:09  tjchol01
% Most of Sherif remarks done.
%
% Revision 1.11  1996/11/24 23:09:48  tjchol01
% Some of Sherif remarks incorporated.
%
% Revision 1.10  1996/11/20 16:43:35  tjchol01
% Increased tocdepth.  Added degree type options.  A bit of cleanup.
%
% Revision 1.9  1996/08/05 03:57:25  tjchol01
% Removed extra chapter spacing from LOT and LOF.
%
% Revision 1.8  1996/07/24 05:04:33  tjchol01
% Chapter TOC unindented and dotted.
%
% Revision 1.7  1996/07/16 18:09:19  tjchol01
% Removed the second blank page from the numbering scheme.
%
% Revision 1.6  1996/07/12 18:34:26  tjchol01
% Unbold chapter TOC line.
%
% Revision 1.5  1996/07/11 01:21:35  tjchol01
% After Kamal corrections and subsection modification.
%
% Revision 1.4  1996/07/10 03:38:03  tjchol01
% Changes for Kamal.
%
% Revision 1.3  1996/07/07 22:21:19  tjchol01
% Next distribution.
%
% Revision 1.2  1996/07/07 19:49:11  tjchol01
% What Brian used for 3 weeks.
%
% Revision 1.1  1996/06/19 04:54:02  tjchol01
% Initial revision
% -------------------------------------------------------------------------
% Local Variables:
% TeX-master: "uofl-example.tex"
% End:
