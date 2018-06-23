#include <stdio.h>
#include <stdlib.h>
#include<string.h>
#include<math.h>
#include<ctype.h>
#define PATH_SIZE 100

typedef struct codeString {
    unsigned int bit : 1 ;
} oneBit;

struct {
    int a : 8 ;
    int b : 8 ;
    int c : 8 ;
    int d : 8 ;
}p ;

int getInfo( FILE *in, int *size, int *offset, int *width, int *BpP )  // Returns 0 if picture is not bitMap
{
    int *tmp ;
    fseek( in, 0, SEEK_SET );
    if ( !(getc(in)=='B') || !(getc(in)=='M') )
        return 0 ;

    fseek( in, 2, SEEK_SET );
    p.a = getc(in);
    p.b = getc(in);
    p.c = getc(in);
    p.d = getc(in);
    tmp = &p;
    *size = *tmp ;

    fseek( in, 10, SEEK_SET );
    p.a = getc(in);
    p.b = getc(in);
    p.c = getc(in);
    p.d = getc(in);
    tmp = &p;
    *offset = *tmp;

    fseek( in, 18, SEEK_SET );
    p.a = getc(in);
    p.b = getc(in);
    p.c = getc(in);
    p.d = getc(in);
    tmp = &p;
    *width = *tmp;

    fseek( in, 28, SEEK_SET );
    p.a = getc(in);
    p.b = getc(in);
    p.c = 0;
    p.d = 0;
    tmp = &p;
    *BpP = *tmp;

    return 1 ; // shows the picture is bitmap
}

void putSize( unsigned char *header, int counter )
{
    int i = 9 ; // put first data in 9th elemet of array
    while ( i>5 )
    {
        header[i--] = counter%256 ;
        counter /= 256 ;
    }
}

int getSize( unsigned char *Header )
{
    int *tmp ;
    p.a = Header[9];
    p.b = Header[8];
    p.c = Header[7];
    p.d = Header[6];
    tmp = &p;
    return *tmp;
}

void giveBinary( int c, oneBit *bin )  // fill the bin with binary code of c
{
    int i;
    for( i=0; i<8; i++ )
        bin[i].bit=0;

    i = 7 ;
    while ( c != 0 )
    {
        bin[i--].bit = c%2 ;
        c /= 2 ;
    }

}

int giveAscii( oneBit *bin )
{
    short int i = 0 ;
    while ( bin[i].bit == 0 )
        i++ ;

    short int j = 7-i ;
    int ascii = 0;
    while ( i<8 )
        ascii += ( pow(2,j--) ) * (bin[i++].bit);

    return ascii ;
}

void stegano( char *fileName, char *bitmapFile )
{
    FILE *file = fopen( fileName, "r" );
    FILE *bmp = fopen( bitmapFile, "rb" );
    if ( !file ) {
        printf( "Can not open Text file addressed : %s\n", fileName );
        return ;
    }
    if ( !bmp ) {
        printf( "Can not open Picture file addressed : %s\n", bitmapFile );
        return ;
    }

    FILE *out = fopen( "NEW.bmp" , "wb" );
    if ( !out ) {
        printf( "Can not creat Picture in this location , Permission Denied !!!\n");
        return ;
    }

    char c;
    int i;
    unsigned int codeCounter = 0;
    unsigned int len = 0;
    oneBit binary[8];

    int size, offset, width, BpP ;
    if ( !getInfo(bmp, &size, &offset, &width, &BpP) ) {
        printf( "Input picture is not Bitmap\n" );
        return ;
    }
    if ( BpP != 24 ) {
        printf("Please make sure that yout bitmap is 24 bit/pixel\n");
        return ;
    }

    fseek( file, 0, SEEK_END );
    len = ftell(file);
    fseek( file, 0, SEEK_SET );

    oneBit *codeArray = ( oneBit* )calloc( len*8, sizeof(oneBit) );

    while ( (c = getc(file))!=EOF )
    {
        giveBinary(c, binary );                               /// DO WE NEED & IN HERE ?
        for( i=0; i<8; i++ )
            codeArray[codeCounter++].bit = binary[i].bit;
    }

    if ( codeCounter > ( (size-offset)*2) )
    {
        printf("There is not enought space to holding information !!!\a\n");
        printf("The max size that this picture can hide is : %d Kb\n", (((size-offset)*2)/8)/1000 ) ;
        return ;  // 5
    }

    fseek( bmp, 0, SEEK_SET );
    unsigned char header[offset];
    for( i=0; i<offset; i++ )
        header[i] = getc(bmp);

    putSize( header, codeCounter );
    fwrite( header, 1, offset, out );

    int passer = 0 ;  //number of code we have put in bmp

    while ( !feof(bmp) )
    {
        c = getc(bmp);
        if ( passer < codeCounter )
        {
            if ( (c&1) == 1 )                        // the first bit is 1
                if ( codeArray[passer].bit == 0 )
                    c -= 1 ;
            if ( (c&1) == 0 )                    // the first bit is zero
                if ( codeArray[passer].bit == 1 )
                    c += 1 ;
            passer++ ;


            if ( (c&2) == 2 )                             // the second bit is 1
                if ( codeArray[passer].bit == 0 )
                    c -= 2 ;                            // change second bit to 0
            if ( (c&2) == 0 )                     // the second bit is zero
                if ( codeArray[passer].bit == 1 )
                    c += 2 ;
            passer++ ;

        }
        putc( c, out );
    }


    free(codeArray);
    fclose( out );
    fclose( bmp );
    fclose(file);

}

void deStagano( char *bitmapFileName )
{
    FILE *bmp = fopen( bitmapFileName, "rb" );
    if ( !bmp ) {
        printf( "Can not open Picture file addressed : %s\n", bitmapFileName );
        return ;  // 2
    }
    int i ;  // loops variable

    // reading the picture information
    int size, offset, width, BpP ;
    if ( !getInfo(bmp, &size, &offset, &width, &BpP) ) {
        printf( "Input picture is not Bitmap\n" );
        return ;  // Input file is not bitmap 4
    }

    fseek( bmp, 0, SEEK_SET );
    unsigned char header[offset];  // holding header file
    for( i=0; i<offset; i++ )
        header[i] = getc(bmp);

    int codeSize = getSize( header );  // number of code characters in picture
    if ( codeSize == 0 ) {
        printf ( "Picture is not coded !!!\n" );
        return ;  // 6
    }

    FILE *out = fopen( "TEXT.txt", "w" );
    if ( !out ) {
        printf( "Can not creat TXT File in this location , Permission Denied !!!\n");
        return ;  // 3
    }

    oneBit bin[8] ; // Holds data from picture and decode it
    char c ;
    int counter = 0 ;

    while ( counter < codeSize )
    {
        for ( i=0; i<8; i+=2 )
        {
            c = getc( bmp );

            if ( (c&1) == 1 )
                bin[i].bit = 1;
            if ( (c&1) == 0 )
                bin[i].bit = 0;


            if ( (c&2) == 2 )
                bin[i+1].bit = 1;
            if ( (c&2) == 0 )
                bin[i+1].bit = 0 ;

            counter+=2;
        }
        putc( giveAscii(bin), out );
    }

    fclose(bmp);
    fclose(out);
}


int main( int argc, char *argv[] )
{
    if ( argc > 1 )
    {
        if ( !strcmp(argv[1],"stegano" ) )
        {
            if ( argc > 3 )
                stegano(argv[2], argv[3]);
            else
                printf ( "Not enough input variables\n");
        }
        else if ( !strcmp(argv[1],"destegano") )
        {
            if ( argc > 2 )
                deStagano(argv[2]);
            else
                printf ( "Not enough input variables\n");
        }
        else
            printf ( "Command does not exist, Try \"stegano\" or \"destegano\"\n" );
    }
    else
        printf ( "Not enough input variables\n");
    return 0;
}
