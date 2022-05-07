\documentclass[12pt]{article}
\usepackage[utf8]{ctex}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{minted}
\usepackage{dirtree}
\usepackage{amsmath}

% 算法分页，防止跑到最后
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{float}  
\usepackage{lipsum}
\makeatletter
\newenvironment{breakablealgorithm}
{% \begin{breakablealgorithm}
 \begin{center}
  \refstepcounter{algorithm}% New algorithm
  \hrule height.8pt depth0pt \kern2pt% \@fs@pre for \@fs@ruled
  \renewcommand{\caption}[2][\relax]{% Make a new \caption
   {\raggedright\textbf{\ALG@name~\thealgorithm} ##2\par}%
   \ifx\relax##1\relax % #1 is \relax
   \addcontentsline{loa}{algorithm}{\protect\numberline{\thealgorithm}##2}%
   \else % #1 is not \relax
   \addcontentsline{loa}{algorithm}{\protect\numberline{\thealgorithm}##1}%
   \fi
   \kern2pt\hrule\kern2pt
  }
 }{% \end{breakablealgorithm}
  \kern2pt\hrule\relax% \@fs@post for \@fs@ruled
 \end{center}
}
\makeatother

\include{defs}

\usepackage{lipsum}

%%%%%%%%%%%%%%%
% Title Page
\title{开发报告}
\author{杨亦凡 \ \ 3019234258 \newline 李自安 \ \ 3019207257 \newline 石昊 \ \ \ \ \ \ \ 3019208051 \newline 华溢 \ \ \ \ \ \ \ 3019244091}
\date{\today}
%%%%%%%%%%%%%%%

\begin{document}
\maketitle

\tableofcontents
\clearpage

\section{项目简介}
本项目针对 SQL - - 语言开发了一个编译器前端，包括词法分析器和语法分析器：
\begin{enumerate}
    \item[(1)] 使用自动机理论编写词法分析器
    \item[(2)] 使用自下而上的语法分析方法编写语法分析器
\end{enumerate}

\subsection{开发环境}
macOS Monterey 12.3.1

\subsection{实现语言}
Python 3.9

\subsection{项目结构}
\centering
\includegraphics[width=0.85\textwidth]{codestruct.pdf}

\begin{verbatim}
    ./src/lexer/lexical_analyzer.py 是词法分析器主程序
    ./src/LR1_parser/LR1.py 是语法分析器主程序
    ./tests 是测试用例文件夹
    ./output/token_table 是 token 序列输出
    ./output/parse_result 是规约序列输出
\end{verbatim}

\section{词法分析器}
词法分析器首先用 SQL - - 语言所有单词符号对应的正则表达式通过正则表达式转 NFA 算法构建相应的 NFA，再通过 NFA 确定化算法构建相应的 DFA，然后通过 DFA 最小化算法构建有限自动机，最后根据有限自动机编程实现 SQL - - 语言的词法分析器。

\subsection{需求分析}
词法分析器的输入为 SQL - - 语言源代码，词法分析器识别单词的二元属性并生成符号表，将待分析代码转化为语法分析器可接受的序列。单词符号的类型包括关键字，标识符，界符，运算符，整数，浮点数，字符串。
每种单词符号的具体要求如下：
\begin{table}[!h]
\centering
\caption{关键字（KW，规定为大写）}
\begin{tabular}{ll}
\toprule
类别 & 语法关键字\\
\midrule
 查询表达式     &  (1) SELECT, (2) FROM, (3) WHERE, (4) AS ,(5) * \\
 插入表达式     &  (6) INSERT, (7) INTO, (8) VALUES, (9) VALUE, (10) DEFAULT \\
 更新表达式     &  (10) UPDATE, (11) SET \\
 删除表达式     &  (13) DELETE \\
 连接操作       &  (14) JOIN, (15) LEFT, (16) RIGHT, (17) ON \\
 聚合操作       &  (18) MIN, (19) MAX, (20) AVG, (21) SUM \\
 集合操作       &  (22) UNION, (23) ALL \\
 组操作         &  (24) GROUP BY, (25) HAVING, (26) DISTINCT, (27) ORFER BY \\
 条件语句       &  (28) TRUE, (29) FALSE, (30) UNKNOWN, (31) IS, (32) NULL \\
\bottomrule
\label{KW}
\end{tabular}
\end{table}

\begin{table}[!h]
\centering
\caption{运算符（OP，规定为大写）}
\begin{tabular}{ll}
\toprule
类别 & 语法关键字\\
\midrule
 比较运算符     &  (1) =, (2) >, (3) <, (4) >= ,(5) <=, (6) !=, (7) <=>  \\
 逻辑运算符     &  (8) AND, (9) \&\&, (10) OR, (11) ||, (12) XOR, (13) NOT, (14) ! \\
 算术运算符     &  (13) - \\
 属性运算符     &  (13) . \\
\bottomrule
\label{OP}
\end{tabular}
\end{table}

\begin{table}[!h]
\centering
\caption{界符（SE）}
\begin{tabular}{ll}
\toprule
类别 & 语法关键字\\
\midrule
 界符     &  (1) (, (2) ), (3) , \\
\bottomrule
\label{SE}
\end{tabular}
\end{table}

标识符（IDN）为字母、数字和下划线（\_）组成的不以数字开头的串;

整数（INT）、浮点数（FLOAT）的定义与 C 语言\textbf{正数}相同，负数通过在正数前面加算术运算符（-）实现;

字符串（STRING）定义与 C 语言相同，使用\textbf{双引号}包含的任意字符串。

\subsection{数据结构描述}

\subsubsection{符号表项}

\begin{center}
TokenLine 抽象数据类型
\begin{verbatim}
    ADT TokenLine {
        数据对象：D = {
            待测代码中的单词符号 word_content,
            单词符号大类 word_type,
            单词符号种别 token_type,
            单词符号内容 token_content
            }
        数据关系：R = {
            <word_content, word_type>,
            <word_type, token_type>,
            <token_type, token_content>
        }
        基本操作：
            input_raw_line(word_content, word_type)
                初始条件：word_content 存在，word_type 合法
                操作结果：产生 token_type，产生 token_content
            output_token_line()
                初始条件：word_content 存在，word_type 合法
                操作结果：产生 token_type，产生 token_content
            _process_raw_line()
                初始条件：word_content 存在，word_type 合法
                操作结果：产生 token_type，产生 token_content
            _get_token_id(token_type)
                初始条件：token_type 存在
                操作结果：返回 word_content 在 token_type 表中对应的序号
    } ADT TokenLine
\end{verbatim}
\label{ADT TokenLine}
\end{center}

\subsubsection{符号表}

\caption{TokenTable 抽象数据类型}
\begin{verbatim}
    ADT TokenTable {
        数据对象：D = {TokenLine i | TokenLine i 是符号表项，i = 0, 1,...,n, n >= 0}
        数据关系：R = {<Ti, Ti+1>| Ti, Ti+1 属于D, i = 0,1,...,n-1}
        基本操作：
            add_token_line(toke_line)
                初始条件：toke_line 存在
                操作结果：将 toke_line 加入到 TokenTable 末尾
            print()
                初始条件：TokenTable 存在
                操作结果：格式化打印 TokenTable
            save(test_name)
                初始条件：TokenTable 存在
                操作结果：格式化存储 TokenTable, 文件名为 test_name
            reset()
                操作结果：重置 TokenLine
    } ADT TokenTable
\end{verbatim}
\label{ADT TokenLine}

\subsubsection{图}

\subsection{算法描述}

\subsubsection{正则表达式转 NFA 算法}

\begin{breakablealgorithm}
	\caption{REGEX TO NFA Algorithm}
    \leftline {\textbf{Inputs}:}
	\leftline {正则表达式 $regex$}
	\leftline {\textbf{Outputs}:}
	\leftline {NFA $M = \{S, \Sigma, \delta, S_0, S_t\}$}
	\begin{algorithmic}[1] %每行显示行号
	    \STATE 对输⼊的正则表达式预处理，将正则表达式中隐含的 \& 补充
	    \STATE 初始化操作符栈 $OPTR$ 和操作数栈 $OPND$
	    \WHILE{$OPTR$[-1] == '\#' and $regex$[i] == '\#'}
	    \STATE 扫描处理后的正则式，读⼊⼀个字符 $ch$
    	    \WHILE {$ch$ 为操作数}
    	    \STATE 将 $ch$ 压⼊ $OPND$，读⼊⼀个字符 $ch$
            \ENDWHILE
	    \STATE ⽐较当前输⼊操作符和操作符栈顶的操作符的优先级
	    \IF {当前输⼊操作符优先级更⾼}
	    \STATE 将 $ch$ 压⼊$OPTR$，读⼊⼀个字符 $ch$
	    \ENDIF
	    \IF {两者优先级相同}
	    \STATE 弹出 $OPTR$ 栈顶元素，读⼊⼀个字符 $ch$
	    \ENDIF
	    \IF {当前输⼊操作符优先级更低}
	    \STATE 弹出 $OPTR$ 栈顶元素，根据其具体类别弹出 $OPND$ 1 个或 2 个操作数，⽣成相应的状态图并压⼊ $OPND$
	    \ENDIF
	    \ENDWHILE
	\end{algorithmic} 
	\label{algorithm1}
\end{breakablealgorithm}

\subsubsection{NFA 确定化算法}

\begin{breakablealgorithm}
	\caption{NFA TO DFA Algorithm}
	\leftline {\textbf{Inputs}:}
	\leftline {NFA $M = \{S, \Sigma, \delta, S_0, S_t\}$}
	\leftline {\textbf{Outputs}:}
	\leftline {DFA $M^{'} = \{ S, \Sigma, \delta, S_0, S_t\}$}
	\begin{algorithmic}[1] %每行显示行号
	    \STATE 从 $M$ 的 $S_0$ 出发，将仅经过任意条 $\varepsilon$ 弧能到达的状态组成的集合 $I$ 作为 $M^'$ 的初态 $q_0$
	    \WHILE{不再产生新的状态} 
	    \STATE 从 $I$ 中元素出发，将经过任意 $a \in \Sigma $ 的 $a$ 弧转换 $I_a$ 所组成的集合作为 $M^'$ 的状态
	    \ENDWHILE
	\end{algorithmic} 
	\label{algorithm2}
\end{breakablealgorithm}

\subsubsection{DFA 最小化算法}

\begin{breakablealgorithm}
    \caption{DFA Minimization Algorithm}
    \leftline {\textbf{Inputs}:}
	\leftline {DFA $M = \{ S, \Sigma, \delta, S_0, S_t\}$}
	\leftline {\textbf{Outputs}:}
	\leftline {DFA $M^{'} = \{ S, \Sigma, \delta, S_0, S_t\}$}
    \begin{algorithmic}[1]
	    \STATE 构造状态集的初始划分 $\Pi$，包含终态 $S_t$ 和 非终态 $S - S_t$ 两组
	    \WHILE{not done}
	    \STATE 对 $Pi$ 使用传播性原则构造新划分 $\Pi_{new}$
	    \IF {$\Pi_{new}$ == $\Pi$}
	    \STATE $\Pi_{final}$ == $\Pi$ \ done
	    \ELSE
	    \STATE $\Pi$ == $\Pi_{new}$
	    \ENDIF
	    \ENDWHILE
	    \FOR {all $\Pi_{final}$}
	    \STATE 选一代表元素 $s$，加入到 $M'$ 的 $S$
	    \IF {代表$s$满足$\delta(s,a)==t$}
	    \STATE 令 $r$ 作为 $t$ 组的代表，将转换 $\delta(s,a)=r$ 加入到 $M'$ 的 $\delta$
	    \ENDIF 
	    \STATE 将含有 $S_0$ 的组的代表作为 $M'$ 的开始状态
	    \STATE 将含有 $S_t$ 的组的代表作为 $M'$ 的终态
	    \ENDFOR
	    \STATE 去除 $M'$ 的 $S$ 中死状态
    \end{algorithmic}
    \label{algorithm3}
\end{breakablealgorithm}

\subsubsection{去除注释算法}

\begin{breakablealgorithm}
    \caption{Input Preprocessing Algorithm}
    \leftline {\textbf{Inputs}:}
	\leftline {带注释的SQL - - 语言源代码 $Text_{raw}$}
	\leftline {\textbf{Outputs}:}
	\leftline {去除注释的SQL - - 语言源代码 $Text_{preprocessed}$}
    \begin{algorithmic}[1]
        \STATE 当前字符串 $current\_string \gets ""$
        \STATE 当前状态 $state \gets$ 代码
        \FOR {all $ch$ $\in$ $Text_{raw}$}
        \IF {$state$ == 代码} {
            \IF {$ch$ == '/'} {
                \STATE $state$ $\gets$ 斜杠
            }
            \ELSIF {$ch$ == "-"} {
                \STATE $state$ $\gets$ 短横线
            }
            \ELSE {
                \STATE $current\_string$ += $ch$
                \IF {$ch$ == '\textbackslash{'}'} {
                    \STATE $state$ $\gets$ 字符
                }
                \ELSIF {$ch$ == '\textbackslash{"}'} {
                    \STATE $state$ $\gets$ 字符串
                }
                \ENDIF
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 短横线} {
            \IF {$ch$ == '-'} {
                \STATE $state$ $\gets$ 单⾏注释
            }
            \ELSE {
                \STATE $current\_string$ += "-" + $ch$
                \STATE $state$ $\gets$ 代码
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 斜杠} {
            \IF {$ch$ == '*'} {
                \STATE $state$ $\gets$ 多⾏注释
            }
            \ELSIF {$ch$ == '/'} {
                \STATE $state$ $\gets$ 单⾏注释
            }
            \ELSE {
                \STATE $current\_string$ += "/"
                \STATE $current\_string$ += $ch$
                \STATE $state$ $\gets$ 代码
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 多⾏注释} {
            \IF {$ch$ == '*'} {
                \STATE $state$ $\gets$ 多⾏注释遇到*
            }
            \ELSE {
                \IF {$ch$ == '\textbackslash{n}'} {
                    \STATE $current\_string$ += '\textbackslash{r}\textbackslash{n}'
                }
                \STATE $state$ $\gets$ 多⾏注释
                \ENDIF
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 多⾏注释遇到\*} {
            \IF {$ch$ == '/'} {
                \STATE $state$ $\gets$ 代码
            }
            \ELSIF {$ch$ == '*'} {
                \STATE $state$ $\gets$ 多⾏注释遇到\*
            }
            \ELSE {
                \STATE $state$ $\gets$ 多⾏注释
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 单⾏注释} {
            \IF {$ch$ == '\textbackslash{}\textbackslash{}'} { 
                \STATE $state$ $\gets$ 拆⾏注释
            }
            \ELSIF {$ch$ == '\textbackslash{n}'} {
                \STATE $current\_string$ += '\textbackslash{r}\textbackslash{n}'
                \STATE $state$ $\gets$ 代码
            }
            \ELSE {
                \STATE $state$ $\gets$ 单⾏注释
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 拆⾏注释} {
            \IF {$ch$ == '\textbackslash{}\textbackslash{}' OR $ch$ == '\textbackslash{r}' OR $ch$ == '\textbackslash{n}'} {
                \IF {$ch$ == '\textbackslash{n}'} {
                    \STATE $current\_string$ += '\textbackslash{r}\textbackslash{n}'
                }
                \ENDIF
                \STATE $state$ $\gets$ 拆⾏注释
            }
            \ELSE {
                \STATE $state$ $\gets$ 单⾏注释
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 字符} {
            \STATE $current\_string$ += $ch$
            \IF {$ch$ == '\textbackslash{}\textbackslash{}'} {
                \STATE $state$ $\gets$ 字符中的转义字符
            }
            \ELSIF {$ch$ == '\textbackslash{'}'} {
                \STATE $state$ $\gets$ 代码
            }
            \ELSE {
                \STATE $state$ $\gets$ 字符
            }
            \ENDIF
        }
        
        \ELSIF {$state$ == 字符中的转义字符} {
            \STATE $current\_string$ += $ch$
            \STATE $state$ $\gets$ 字符
        }
        
        \ELSIF {$state$ == 字符串} {
            \STATE $current\_string$ += $ch$
            \IF {$ch$ == '\textbackslash{}\textbackslash{}'} {
                \STATE $state$ $\gets$ 字符串中的转义字符
            }
            \ELSIF {$ch$ == '\textbackslash{"}'} {
                \STATE $state$ $\gets$ 代码
            }
            \ELSE {
                \STATE $state$ $\gets$ 字符串
            }
            \ENDIF
        }
        \ELSIF {$state$ == 字符串中的转义字符} {
            \STATE $current\_string$ += $ch$
            \STATE $state$ $\gets$ 字符串
        }
        \ENDIF
        \ENDFOR
    \STATE $Text_{preprocessed}$ += $current\_string$
    \end{algorithmic}
    \label{algorithm4}
\end{breakablealgorithm}

\subsection{输出格式说明}
\subsubsection{正则表达式转 NFA 算法}

\includegraphics[width=0.5\textwidth]{R2N.png}

\subsubsection{NFA 确定化算法}

\includegraphics[width=0.5\textwidth]{N2D.png}

\subsubsection{DFA 最小化算法}

\includegraphics[width=0.5\textwidth]{MD.png}

\subsubsection{Token 序列}
Token 输出格式：
\begin{verbatim}
    [待测代码中的单词符号] [TAB] <[单词符号种别],[单词符号内容]>
\end{verbatim}

其中，单词符号种别为 KW（关键字）、OP（运算符）、SE（界符）、IDN（标识符）、INT （整形数）、FLOAT（浮点数）、STRING（字符串）；单词符号内容 KW、OP、SE 为其编号，KW见表 \ref{KW}，OP见表 \ref{OP}，SE见表\ref{SE}；其余类型为其值。

\subsection{源程序编译步骤}


\section{语法分析器}
\subsection{数据结构描述}
\subsubsection{grammar}
语法分析前需要首先对文法进行预处理，将以文本文件形式存储的语法转换为${\rm [V_N, V_T, P, S]}$的形式





\subsection{算法描述}

\subsubsection{计算语法四元组}
\begin{breakablealgorithm}
    \caption{Load\ grammar}
    \leftline {\textbf{Inputs}:}
	\leftline {grammar.txt}
    \begin{algorithmic}[1]
	    \STATE 初始化: $non\_terminals\leftarrow[\ ], terminals\leftarrow[\ ], productions\leftarrow[\ ], start\leftarrow None$ 
	    \STATE $all\_symbols\leftarrow[\ ], cnt\leftarrow1$
	    \FOR{grammar.txt中的每一个产生式}
        \STATE 将产生式左端符号$append$到$non\_terminals$中
        \STATE 将产生式左端符号$append$到$all\_symbols$中
        \STATE ${\rm initialize}\ production$
        \STATE $production.left\leftarrow$产生式左端符号
        \STATE $production.right\leftarrow$产生式右端符号集
        \STATE $production.idx\leftarrow cnt$
        \STATE $cnt\leftarrow cnt+1$
        \FOR{产生式右端符号$i$}
        \STATE 将产生式右端符号$i\ append$到$all\_symbols$中
        \ENDFOR
        \ENDFOR
        \STATE $Unique(non\_terminals, terminals)$
        \STATE $terminals=all\_symbols-non\_terminals$
        \STATE $start\leftarrow productions[0].left$
        \STATE 初始化$grammar$
        \STATE $grammar.non\_terminals\leftarrow non\_terminals$
        \STATE $grammar.terminals\leftarrow terminals$
        \STATE $grammar.productions\leftarrow productions$
        \STATE $grammar.start\leftarrow start$
        \RETURN $grammar$
    \end{algorithmic}
    \label{algorithm5}
\end{breakablealgorithm}


\subsubsection{求FIRST集}
\begin{breakablealgorithm}
    \caption{Calculate\ First\ Set}
    \leftline {\textbf{Inputs}:}
	\leftline {文法grammar}
    \begin{algorithmic}[1]
        \WHILE{FIRST仍在增大}
        \FOR{$N\ {\rm in}\ grammar.non\_terminals$}
        \STATE $First[N]\leftarrow[\ ]$
        \ENDFOR
        \FOR{$T\ {\rm in}\ grammar.terminals$}
        \STATE $First[T]\leftarrow[T]$
        \ENDFOR
        \FOR{$P\ {\rm in}\ grammar.productions$}
        \IF {$P.right[0]\ {\rm in}\ grammar.erminals$}
        \STATE $First[P.left].append(P.right[0])$
        \ENDIF
        \IF {$P.right=[\ ]$}
        \STATE $First[P.left].append(\varepsilon)$
        \ENDIF
        \IF {$P.right$的左侧含有连续$i$个符号位于$grammar.non\_terminals$中，且对任意$i$, $First[i]$均含$\varepsilon$}
        \STATE $First[P.left].extend(FIRST[i+1]-[\varepsilon])$
        \ENDIF
        \ENDFOR
        \ENDWHILE
        \RETURN $First$
    \end{algorithmic}
    \label{algorithm6}
\end{breakablealgorithm}

\subsubsection{求FOLLOW集}
\begin{breakablealgorithm}
    \caption{Calculate\ Follow\ Set}
    \leftline {\textbf{Inputs}:}
	\leftline {文法grammar, FIRST集}
    \begin{algorithmic}[1]
        \WHILE{FOLLOW仍在增大}
        \FOR{$N\ {\rm in}\ grammar.non\_terminals$}
        \STATE $Follow[N]\leftarrow[\ ]$
        \ENDFOR
        \STATE $Follow[grammar.start]\leftarrow[$\#$]$
        \FOR{$P\ {\rm in}\ grammar.productions$}
        \IF {$P$的形式为$A\rightarrow\alpha B\beta$,其中$A,B$位于$grammar.non\_terminals$中，$\alpha ,\beta$为任意符号串}
        \STATE $Follow[B].extend(FIRST[\beta]-[\varepsilon])$
        \ENDIF
        \IF {$P$的形式为$A\rightarrow\alpha B$,其中$A,B$位于$grammar.non\_terminals$中，$\alpha$为任意符号串}
        \STATE $Follow[B].extend(Follow[A])$
        \ENDIF
        \IF {$P$的形式为$A\rightarrow\alpha B\beta$,其中$A$位于$grammar.non\_terminals$中，$\alpha ,\beta$为任意符号串，且$\varepsilon$含在$First[\beta]$中}
        \STATE $Follow[B].extend(Follow[A])$
        \ENDIF
        \ENDFOR
        \ENDWHILE
        \RETURN $Follow$
    \end{algorithmic}
    \label{algorithm7}
\end{breakablealgorithm}

\subsubsection{求闭包}
\begin{breakablealgorithm}
    \caption{Calculate\ Closure}
    \leftline {\textbf{Inputs}:}
	\leftline {文法grammar, FIRST集, FOLLOW集, 项目集I}
    \begin{algorithmic}[1]
        \STATE $closure[I]\leftarrow[\ ]$
        \FOR{$i\ {\rm in}\ I$}
        \STATE $closure[I].append(i)$
        \ENDFOR
        \WHILE {$closure[I]$仍在增大}
        \FOR {$item$ {\rm in} $closure[I]$}
        \IF {$item$的形式为$A\rightarrow\alpha·B\beta, a$,其中$A,B$位于$grammar.non\_terminals$中，$\alpha,\beta$为任意符号串,$a$位于$grammar.terminals$中}
        \FOR {$grammar.productions$中所有满足$P.left=B$的$P$}
        \FOR {所有$b$ {\rm in} $grammar.terminals$,并且$b$位于$First[\beta a]$中}
        \STATE $closure[I].append(B\rightarrow· \gamma, b)$
        \ENDFOR
        \ENDFOR
        \ENDIF
        \ENDFOR
        \ENDWHILE
        \RETURN $closure[I]$
    \end{algorithmic}
    \label{algorithm6}
\end{breakablealgorithm}

\subsubsection{求项目集规范族与GO}
\begin{breakablealgorithm}
    \caption{Calculate\ Item\ Set\ and GO}
    \leftline {\textbf{Inputs}:}
	\leftline {文法grammar, FIRST集, FOLLOW集}
    \begin{algorithmic}[1]
        \STATE 初始化：$itemset\leftarrow[\ ]$
        \STATE $itemset.append(grammar.start\rightarrow· grammar.right, \#)$
        \STATE $itemset[0] \leftarrow closure[itemset[0]]$
        \STATE 计算$itemset[0]$可以GO到项目集Is，其中$GO(itemset[0],A)=closure[J]$,其中$J=$\{任何形如$[A\rightarrow\alpha B·\beta,a]$的项目$|[A\rightarrow\alpha·B\beta,a]$在$itemset[0]$中
    $\}$.同时将相应的GO关系加入GO中。
        \FOR {$I\ {\rm in}\ Is$}
        \STATE $itemset.append(I)$
        \ENDFOR
	    \WHILE{itemset仍在增大}
        \FOR{$I\ {\rm in}\ itemset$}
        \STATE 计算$I$可以GO到项目集$Is$，其中$GO(itemset[0],A)=closure[J]$,其中$J=$\{任何形如$[A\rightarrow\alpha B·\beta,a]$的项目$|[A\rightarrow\alpha·B\beta,a]$在$itemset[0]$中
    $\}$.同时将相应的GO关系加入GO中。
        \FOR {$I\ {\rm in}\ Is$ AND $I$不在itemset中}
        \STATE $itemset.append(I)$
        \ENDFOR
        \ENDFOR
        \ENDWHILE
        \RETURN $itemset,\ GO$
    \end{algorithmic}
    \label{algorithm9}
\end{breakablealgorithm}

\subsubsection{求ACTION表与goto表}
\begin{breakablealgorithm}
    \caption{Calculate\ Analysis\ Table}
    \leftline {\textbf{Inputs}:}
	\leftline {项目集规范族itemsets, GO关系, 文法grammar}
    \begin{algorithmic}[1]
        \FOR {$itemset \in\ itemsets$}
        \FOR {$I \in\ itemset$}
        \IF {I的形式为$[A-> \alpha·a\beta,\ b]$，且$Go[I,a]=I_j$，$a$在$grammar.terminal$中}
        \STATE $action[itemset.idx,a] \leftarrow s_j$
        \ENDIF
        \IF {I的形式为$[A-> \alpha·, a]$}
        \STATE $action[itemset.idx,a] \leftarrow r_j$，其中$r_j$为$I$的编号
        \ENDIF
        \IF {I的形式为$[grammar.start_p->grammar.start·,\#]$}
        \STATE $action[itemset.idx,\#] \leftarrow acc$
        \ENDIF
        \IF {不满足以上所有情况}
        \STATE 抛出错误
        \ENDIF
        \ENDFOR
        \ENDFOR
        \FOR {$go\ {\rm in}\ GO$}
        \STATE $goto[go.idx,go.symbol] \leftarrow go.next$
        \ENDFOR
        \RETURN $action, goto$

    \end{algorithmic}
    \label{algorithm10}
\end{breakablealgorithm}

\subsubsection{LR1的parse解析过程}
\begin{breakablealgorithm}
    \caption{Parse}
    \leftline {\textbf{Inputs}:}
	\leftline {待解析的$input\_stack(token$序列$)$以及$action, goto, $文法$grammar$}
    \begin{algorithmic}[1] 
        \STATE 初始化：$state\_stack = Stack(),\ symbol\_stack = Stack()$
        \STATE 初始化：$state\_stack.push(0),\ symbol\_stack.push(\#)$
        \WHILE {$input\_stack$不空}
        \STATE $top\_state = state\_stack.top(),\ top\_symbol = symbol\_stack.top()$
        \IF {$top\_symbol = \#\ or\ top\_symbol\ {\rm in}\ grammar.terminal$}
        \STATE $action\_now \leftarrow action[top\_state,\ top\_symbol]$
        \IF {$action\_now = acc$}
        \STATE 将$top\_symbol,\ top\_state$与$acc$等信息打印
        \STATE 解析成功
        \RETURN
        \ENDIF
        \IF {$action\_now = None$}
        \STATE 将$top\_symbol,\ top\_state$与$err$等信息打印
        \STATE 语法错误
        \RETURN
        \ENDIF
        \IF {$action\_now[0] = s$}
        \STATE 将$top\_symbol,\ top\_state$与$move$等信息打印
        \STATE 将$action\_now.state$压入$state\_stack$, $input\_stack.peak()$压入$symbol\_stack$, 将$input\_stack$栈顶元素弹出
        \ENDIF
        \IF {$action\_now[0] = r$}
        \STATE 将$top\_symbol,\ top\_state$与$redution$等信息打印
        \STATE 按照$action\_now.state$对应的$grammar$将$symbol\_stack$栈顶几个元素进行规约，并将规约结果压入$symbol\_stack$
        \STATE 根据$symbol\_stack.top()$与当前状态$top\_state$查找$goto$表，将$goto$表中的结果压入$state\_stack$
        \ENDIF  
        \ENDIF
        \IF {$top\_symbol\ {\rm in}\ grammar.non\_terminals$}
        \STATE $goto\_now \leftarrow goto[top\_state,\ top\_symbol]$
        \IF {$goto\_now = None$}
        \STATE 将$top\_symbol,\ top\_state$与$err$等信息打印
        \STATE 语法错误
        \RETURN
        \ENDIF
        \IF {$goto_now[0] = s$}
        \STATE 将$top\_symbol,\ top\_state$与$move$等信息打印
        \STATE 将$goto\_now.state$压入$state\_stack$, $input\_stack.peak()$压入$symbol\_stack$, 将$input\_stack$栈顶元素弹出
        \ENDIF
        \ENDIF
        \ENDWHILE

    \end{algorithmic}
    \label{algorithm11}
\end{breakablealgorithm}

\subsection{LR1分析表描述}

\subsection{输出格式说明}   
\subsubsection{FIRST集与FOLLOW集输出}
FIRST集每一行的输出格式：
\begin{verbatim}
    [符号（终结符或非终结符）] [=] [符号对应的FIRST集]
\end{verbatim}


输出示例：\\

    \centering
    \includegraphics[width=0.15\textwidth]{first.jpg}


FOLLOW集每一行的输出格式：

\begin{verbatim}
    [符号（终结符或非终结符）] [=] [符号对应的FOLLOW集]
\end{verbatim}

输出示例：

    \centering
    \includegraphics[width=1.0\textwidth]{follow.jpg}



\subsubsection{项目集规范族输出}
项目集规范族中每一个项目集的输出格式：

\begin{verbatim}
    [itemset] [项目集在项目集规范族中的序号] [:] [\n]
    [项目1] [\n]
    [项目2] [\n]
    ......
    [项目n] [\n][\n]
\end{verbatim}

其中，项目的输出格式如下：

\begin{verbatim}
    [左侧符号] [, ] [右侧符号集] [, ] [dot位置] [, ] [终结符号集] [, ] [产生式序号]
\end{verbatim}

输出示例：

    \centering
    \includegraphics[width=1.0\textwidth]{itemsets.jpg}



项目集规范族各项目集之间的转移关系go的输出格式：

\begin{verbatim}
    [(][(][当前项目集序号][,][面临符号][)][,][转移后的项目集序号][)]
\end{verbatim}

输出示例：


    \centering
    \includegraphics[width=0.4\textwidth]{go.jpg}



\subsubsection{LR1分析表输出}
LR1分析表包括action表和goto表两个部分，二者分别输出。\\

其中：

action表输出格式：

\begin{verbatim}
    [(] [当前状态] [,] [面临输入符号] [)] [  ---->  ] [动作类型] [动作值]
\end{verbatim}

在action表中，面临输入符号限定为非终结符，动作类型的可选值为：s、r、acc、None（表示不存在该动作，与err等价）。

输出示例：

    \centering
    \includegraphics[width=0.3\textwidth]{action.jpg}



goto表输出格式：

\begin{verbatim}
    [(] [当前状态] [,] [面临输入符号] [)] [  ---->  ] [动作类型(s或None)] [动作值]
\end{verbatim}

在goto表中，面临输入符号限定为终结符，动作类型的可选值：s、None（表示不存在该动作，与err等价）。
输出示例：

    \centering
    \includegraphics[width=0.46\textwidth]{goto.jpg}





\subsubsection{规约序列输出}
规约序列每一行的输出格式：
\begin{verbatim}
    [序号] [TAB] [选用规则序号] [TAB] [栈顶符号]#[面临输入符号] [TAB] [执行动作]
\end{verbatim}

其中，选用规则序号见附件文法规则；执行动作为“reduction”（归约），“move”（LR 分析的移进），“accept”（接受）或 “error”（错误）
输出示例：




    \centering
    \includegraphics[width=0.4\textwidth]{parse_result.jpg}



\subsection{源程序编译步骤}


\end{document}  
