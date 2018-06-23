%{
    #include "y.tab.h"
    #include "calc.h"
    #include <string.h>

    enum { EQ, LE, GE, LT, GT, NE };

%}

%option noyywrap

DIGIT   [0-9]
ID      [_[:alpha:]][_[:alnum:]]*
NUM     [-+]?{DIGIT}+
FLOAT   [-+]?{DIGIT}+"."({DIGIT}+(E[+-]{DIGIT}+)?)?


%%
[ \t\n]+      /* Ignore */

if          return IF;
else        return ELSE;
while       return WHILE;
do          return DO;
for         return FOR;
[-+*/^=]    return yytext[0];
[(){};]     return yytext[0];
"||"        return OR;
"&&"        return AND;

"<"         yylval.relType = LT; return RELOP;
">"         yylval.relType = GT; return RELOP;
">="        yylval.relType = GE; return RELOP;
"<="        yylval.relType = LE; return RELOP;
"=="        yylval.relType = EQ; return RELOP;
"!="        yylval.relType = NE; return RELOP;

{NUM}   {
        yylval.lexem.str = strdup( yytext );
        yylval.lexem.printed = 0;
        return NUM;
}

{ID}    {
        yylval.lexem.str = strdup( yytext );
        yylval.lexem.printed = 0;
        return ID;  /* Lex uses this value to recognize the token */
}
    
.       { printf("\nUnknown character : %c\n", yytext[0]); }
%%

