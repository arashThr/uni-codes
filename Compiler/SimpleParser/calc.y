%{
    /* PROLOGUE
    Define types and variables used in the actions, preprocessor commands
    */
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ncurses.h>
    #include "calc.h"
    #define TRUE 1
    #define FALSE 0
    #define BUF_SIZE 512
    #define STEP 4

    /* YYSTYPE, the C data type for semantic values of both tokens and groupings. Defualt : int 
    #define YYSTYPE char * */

    enum { EQ, LE, GE, LT, GT, NE };
    enum { DIRECTIVE, ROOT, EXPR  };

    void yyerror( const char *);
    int yylex();
    int yywrap();

    void printRoot( const char * );
    void printNode( const char * );

    char buf[BUF_SIZE];

    int col=0;
    int row=0;
    int tmp=0;
%}

/* Union specifies the entire list of possible types, instead of YYSTYPE */
%union {
    struct {
        char *str;
        int printed;
    } lexem;
    int relType;
}


/* We need to associate a type with each grammar symbol whose semantic value is used ( we've used union )*/
%token  <lexem> IF ELSE WHILE DO FOR NUM ID AND OR
%token  <relType> RELOP
%type   <lexem> exp

%right '='
%nonassoc RELOP
%nonassoc OR
%left '+' '-'
%left '*' '/'
%left '(' ')'

/* pseudo-variable `$$' : the semantic value for the grouping that the rule is going to construct */
/* pseudo-variable `@N', `@$' : reach locations inside of semantic actions */
%%

program :    block { exit(0); printf("Fully parsed\n"); }
;
block   :   '{' stmts '}'
;
stmts   :   /* empty */
        |   stmts stmt
;

stmt    :   exp ';' { col = tmp; }
        
        |   WHILE '(' { printRoot("WHILE"); tmp = col+STEP; printRoot("COND:"); } exp ')'
            { col = tmp-STEP; printRoot("BODY:"); } stmt { col = 0; }

        |   IF '(' { printRoot("BRANCH"); tmp = col; printRoot("COND:"); } exp ')'
            { col = tmp; printRoot("IF:"); } stmt rest { col=tmp ; }

        |   block
        |   error '\n'  { yyerrok; } /* yyerrok means error recovery is complete */
;


rest    :   
        |   ELSE { printRoot("ELSE"); tmp = col+STEP; } stmt { col=tmp; }


exp :   NUM             { $$.str = strdup($1.str); }
    |   ID              { $$.str = strdup($1.str); }
    |   exp RELOP exp {
        if ( $2 == GT ) {
            if ( ! $1.printed ) { printNode( $1.str ); $1.printed = TRUE; }
            if ( ! $3.printed ) { printNode( $3.str ); $3.printed = TRUE; }
            printRoot(">"); $$.printed=TRUE;
        }
        if ( $2 == LT ) {
            if ( ! $1.printed ) { printNode( $1.str ); $1.printed = TRUE; }
            if ( ! $3.printed ) { printNode( $3.str ); $3.printed = TRUE; }
            printRoot("<"); $$.printed=TRUE;
        }
    }
    |   exp '=' exp { 
            if ( ! $1.printed ) { printNode( $1.str ); $1.printed = TRUE; }
            if ( ! $3.printed ) { printNode( $3.str ); $3.printed = TRUE; }
            printRoot("="); $$.printed=TRUE;
            
        }
    |   exp '+' exp { 
            if ( ! $1.printed ) { printNode( $1.str ); $1.printed = TRUE; }
            if ( ! $3.printed ) { printNode( $3.str ); $3.printed = TRUE; }
            printRoot("+"); $$.printed=TRUE;
        }
    |   exp '-' exp { 
            if ( ! $1.printed ) { printNode( $1.str ); $1.printed = TRUE; }
            if ( ! $3.printed ) { printNode( $3.str ); $3.printed = TRUE; }
            printRoot("-"); $$.printed=TRUE;
        }
    |   '(' exp ')' {
            if ( ! $2.printed ) { printNode( $2.str ); $2.printed = TRUE; }
            $$.printed = TRUE;
        }
;

%%

    //|   exp '=' exp { sprintf( buf, "= %s %s", $1, $3 ); $$ = strdup(buf); buf[0]= '\0'; }
    /*|   exp '=' exp { bufNewLevel("="); bufNode($1); bufNode($3);
        bufRemove("\\="); $$ = strdup(buf); buf[0]= '\0'; }
    |   exp '+' exp { bufNewLevel("+"); bufNode($1); bufNode($3);
        bufRemove("\\+"); $$ = strdup(buf); buf[0]= '\0'; }*/
void yyerror( const char *msg ) {
    fprintf( stderr, "Error occurred : %s\n", msg );
}

#define BLANK_SIZE 50
char blank[BLANK_SIZE];


void printRoot( const char *str ) {
    printNode( str );
    col += STEP;
}

void printNode( const char *str ) {
    row += 1;
    mvaddstr( row, col, str );
    refresh();
}


int main() {
    /* Returns 0 on successful, 1 otherwise -> Calls yyerror routin */
    int i;
    for ( i=0; i<BLANK_SIZE; i++ )
        blank[i] = ' ';
    blank[0] = '\0';
    
    initscr();
    refresh();

    return yyparse();

    endwin();
}


/* How to compile :
    |   exp '^' exp     { $$ = pow( $1, $3 ); }
bison -vdty calc.y
flex calc.l
gcc *.c -ll

    |   exp '=' exp { sprintf( $$, "%s = %s", $1, $3 ); printf("1: %s\n3: %s\n", $1, $3);}
    |   exp '+' exp { sprintf( $$, "%s + %s", $1, $3 ); printf("1-2: %s\n3-2: %s\n", $1, $3);}

{
a = ( 1 + 4 );
1-2: 1 + 4
3-2: 4

PARAN : 1 + 4
1: ( 1 + 4 ) = ( 1 + 4 ) = (
3: ( 1 + 4 ) = ( 1 + 4 ) = (
 ( 1 + 4 ) = ( 1 + 4 ) = (

    |   '(' exp ')' { sprintf( $$, "( %s )", $2 ); printf("\nPARAN : %s\n", $2);}

Note that we have implemented yyerror ourself and we do not use -ly

        |   FOR '(' init ';' exp ';' exp ')'
            { newLevel("FOR"); printNode("INIT:", DIRECTIVE); printNode($3, EXPR); printNode("COND:", DIRECTIVE);
            printNode($5, EXPR); printNode("STEP", DIRECTIVE); printNode($7, EXPR); printNode("BODY:", DIRECTIVE); }
            stmt { removeLevel("ROF"); }
 

*/
