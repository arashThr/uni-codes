bison -vdty calc.y
flex calc.l
gcc lex.yy.c y.tab.c -ll -lncurses
