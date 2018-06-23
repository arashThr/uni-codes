#ifndef HEADER_H_INCLUDED
#define HEADER_H_INCLUDED

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include<ctype.h>
#include<time.h>

#define True      1
#define False     0
#define ERROR    -1
#define PATH_SIZE 100

typedef struct codeString {
    unsigned int bit : 1 ;
} oneBit;

void stegano         ( char *, char * );  // Text path , Bitmap file path
void deStagano       ( char *         ); // Bitmap coded file path

/************************** Auxiliary Functions ************************************************/
void giveBinary      ( int, oneBit *        );        // input number , fill with binary
int  giveAscii       ( oneBit *             );       // number in binary mode
int  getLine         ( char *, int          );      // Filled with input , max size
void alphaToCode     ( char *, char *       );     // Text File Name , Bitmap File Name
void codeToAlpha     ( oneBit * , int       );    // Array of code characters , length of the code Array
void putSize         ( unsigned char *, int );   // Picture's header , size of code array
int  getSize         ( unsigned char *      );  // Array of pictures header
int  getInfo         ( FILE *in,
                       int  *size,
                       int  *offset,
                       int  *width,
                       int  *BpP       ); // gets the informations of picture

#endif // HEADER_H_INCLUDED
