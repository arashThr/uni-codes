/* Function type */
typedef double (*func_t) (double);

/* Data type for links in chain of symbols */
typedef struct symrec {
    char *name;
    int type;
    union {
        int var;      /* value of a VAR */
        func_t fnctptr;  /* value of a FNCT */
    }value;
    struct symrec *next;
} symrec;

/* The symbol table */
extern symrec *sym_table;

symrec *putsym( char const *, int );
symrec *getsym( char const *);

