%{
/* Compiler project, Phase 1
 * Arash Taher
 */
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define NSYM 100    /* Numbers symbol table rows */
#define ISYM 100    /* ID symbol table rows */
#define MAX_STR_CONST 100   /* Max size of string literals */

/* Define constants in program and associate value to each one*/
enum { IF=1, ELSE, WHILE, DO, FOR, ID, RELOP, EQ, LE, GE, LT, GT, NE };
enum numType { INT, FLOAT, LITERAL, LEXEM };

int line_count = 1;

/* TODO : This value will be updated when we combine this program with parser */
int yylval;
/* We use `scope_depth' to simulate scopes */
/* We didn't fully implement it, because in this area, the project definition is vague */
int scope_depth = 0;

/* Defining symbol table structures for numbers and ids */
int numRows = 0;
int idRows = 0;

struct {
    char *val;
    int valType;    /* INT or FLOAT */
    union {
        int iVal;
        float fVal;
    } u;
} numSymTab[NSYM];

struct {
    int varType;   /* Literal or Lexem */
    int level;    /* Scope of this variable */
    char *lexem;
    char *info;
} idSymTab[ISYM];


/* Install numbers in number's symbol table and return row number */
int installNum( char *num, int type ) ;
int installID( char *text, int type ) ;

%}

/* Defninitions */
DIGIT   [0-9]
ID      [_[:alpha:]][_[:alnum:]]*
FNUM    [-+]?{DIGIT}+"."({DIGIT}+(E[+-]{DIGIT}+)?)?
NUM     [-+]?{DIGIT}+

%%
\n              line_count++; putchar('\n');
[ \t]+$         /* Ignore blanks at the end of lines */
[ \t]+          putchar( ' ' );

_+|[0-9]+[_|[:alpha:]]+|{ID}\.{DIGIT}* { 
    printf("\nError (line %d):\"%s\" -> Unkown token\n", line_count, yytext);
}

"/*"       {
           int c;
           for( ; ; ) {
               while ( ( c = input() ) != '*' &&
                   c != '\0' )     /* Eat up text of comment */
                   if ( c == '\n' )
                       line_count++;
               if ( c == '*' ) {
                   while ( ( c = input() ) == '*' );
                   if ( c == '/' ) break ; /* End of comment */
                   else if ( c == '\0' ) {
                       fprintf( stderr, "EOF in comment\n" );
                       break;
                   }
               }

           }
           }


\"         {
           int c;
           /* Literals */
           char string_buf[MAX_STR_CONST];
           char *string_buf_ptr;

           string_buf_ptr = string_buf;
           *string_buf_ptr++ = '\"' ;

           for ( ; ; ) {
               while ( ( c = input() ) != '\"' && c != '\\' && c != '\n' )
                   *string_buf_ptr++ = (char)c ;
               if ( c == '\\' ) {
                   *string_buf_ptr++ = (char)c ;
                   c = input();
                   if ( c == '\n' )
                       *string_buf_ptr++ = 'n' ;
                   else
                       *string_buf_ptr++ = (char)c ;
               }
               else if ( c== '\n' ) {
                   fprintf( stderr, "Unterminating literal\n" );
                   abort();
               }
               else if ( c == '\"' ) {
                   *string_buf_ptr++ = '\"';
                   *string_buf_ptr++ = '\0';
                   yylval = installID( string_buf, LITERAL );
                   printf("<LITERAL, %s>", string_buf);
                   break;
               }
           }
           }


if         printf("IF");
else       printf("ELSE");
while      printf("WHILE");
do         printf("DO");
for        printf("FOR");
\{         printf("{"); scope_depth++;
\}         printf("}"); scope_depth--;
\(         printf("(");
\)         printf(")");
\;         printf(";");
\+         printf("%s", yytext);
\-         printf("%s", yytext);
\*         printf("%s", yytext);
\/         printf("%s", yytext);

"="        printf("<=>");
"+="       printf("<+=>");
"-="       printf("<-=>");
"*="       printf("<*=>");
"/="       printf("</=>");

"=="       yylval = EQ; printf("<==>");
"!="       yylval = NE; printf("<!=>");
"<"        yylval = LT; printf("<`<'>");
">"        yylval = GT; printf("<`>'>");
"<="       yylval = LE; printf("<`<='>");
">="       yylval = GE; printf("<`>='>");

{FNUM}     { printf("<FLOAT, %s>", yytext); 
               yylval = installNum( yytext, FLOAT );  /* Install Float */
           }
{NUM}      { printf("<INT, %s>", yytext);
               yylval = installNum( yytext, INT );    /* Install Integer */
           }
{ID}       { printf("<ID, \"%s\">", yytext);
               yylval = installID( yytext, LEXEM );
           }

.          printf(" %s : UNKNOWN ", yytext);
%%


int main( int argc, char **argv )
{
    ++argv, --argc;  /* skip over program name */
    if ( argc > 0 )
        yyin = fopen( argv[0], "r" );
    else
        yyin = stdin;

    while ( yylex() );

    int i;
    printf("\n\nID Symbol Table :\n");
    for ( i=0; i<idRows; i++ ) {
        if ( idSymTab[i].varType == LEXEM )
            printf("%d lex: %s\n", i, idSymTab[i].lexem);
        else
            printf("%d lit: %s\n", i, idSymTab[i].info);
    }
    printf("Num Symbol Table :\n");
    for ( i=0; i<numRows; i++ )
        printf("%d : %s\n", i, numSymTab[i].val);

    return 0;
}

int yywrap() { return 1; }


/* Install numbers in number's symbol table and return row number */
int installNum( char *num, int type ) {
    numSymTab[numRows].val = strdup( num );
    if ( type == INT ) {
        numSymTab[numRows].valType = INT;
        int tmp = atoi( num );
        numSymTab[numRows].u.iVal = tmp;
    }
    else if ( type == FLOAT ) {
        numSymTab[numRows].valType = FLOAT;
        float tmp = atof( num );
        numSymTab[numRows].u.fVal = tmp;
    }
    else {
        fprintf( stderr, "Error occured\n" );
        abort();
    }
    return numRows++;
}

int installID( char *text, int type ) {
    if ( type == LEXEM ) {
        int i;

        for ( i=0; i<idRows; i++ )
            if ( idSymTab[i].varType == LEXEM &&
                strcmp( idSymTab[i].lexem, text ) == 0 )
                return i;  // This lexem has been already defined

        idSymTab[idRows].varType = LEXEM;
        idSymTab[idRows].level = scope_depth;
        idSymTab[idRows].lexem = strdup( text );
        idSymTab[idRows].info = '\0';
    }
    else if ( type == LITERAL ) {
        idSymTab[idRows].varType = LITERAL;
        idSymTab[idRows].lexem = '\0';
        idSymTab[idRows].info = strdup( text );
    }
    else {
        fprintf( stderr, "Error occured in installID\n" );
        abort();
    }
    return idRows++;
}


