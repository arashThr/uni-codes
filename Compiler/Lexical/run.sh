lex lexical.l
gcc lex.yy.c -o lexical -lfl
./lexical test.c
