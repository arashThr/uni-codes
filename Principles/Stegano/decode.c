#include"Header.h"

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
