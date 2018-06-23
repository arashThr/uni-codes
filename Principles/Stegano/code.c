#include"Header.h"

void stegano( char *fileName, char *bitmapFile )
{
    // Opening files and check them
    FILE *file = fopen( fileName, "r" );
    FILE *bmp = fopen( bitmapFile, "rb" );
    if ( !file ) {
        printf( "Can not open Text file addressed : %s\n", fileName );
        return ;  // 1
    }
    if ( !bmp ) {
        printf( "Can not open Picture file addressed : %s\n", bitmapFile );
        return ;  // 2
    }

    FILE *out = fopen( "NEW.bmp" , "wb" );
    if ( !out ) {
        printf( "Can not creat Picture in this location , Permission Denied !!!\n");
        return ;  // 3
    }

    char c;
    int i;
    unsigned int codeCounter = 0;  // size od code
    unsigned int len = 0;  // length of text
    oneBit binary[8]; // for holding binary of each character

    // Reading the picture information and check verity of picture's type
    int size, offset, width, BpP ;
    if ( !getInfo(bmp, &size, &offset, &width, &BpP) ) {
        printf( "Input picture is not Bitmap\n" );
        return ;  // Input file is not bitmap 4
    }
    if ( BpP != 24 ) {
        printf("Please make sure that yout bitmap is 24 bit/pixel\n");
        return ;
    }

    // Finding length of text
    fseek( file, 0, SEEK_END );
    len = ftell(file);
    fseek( file, 0, SEEK_SET );

    // allocating memory for text changed into binary code
    oneBit *codeArray = ( oneBit* )calloc( len*8, sizeof(oneBit) );

    // Filling code Array with binary code of the characters
    while ( (c = getc(file))!=EOF )
    {
        giveBinary(c, binary );                               /// DO WE NEED & IN HERE ?
        for( i=0; i<8; i++ )
            codeArray[codeCounter++].bit = binary[i].bit;
    }

    // Check picture for haveing enought room
    if ( codeCounter > ( (size-offset)*2) )  // (each byte contains 2 code)
    {
        printf("There is not enought space to holding information !!!\a\n");
        printf("The max size that this picture can hide is : %d Kb\n", (((size-offset)*2)/8)/1000 ) ;
        return ;  // 5
    }

    /******************* Arbitrary *****************************
    *************Gives you binary coded test *******************

    FILE *out = fopen( "OUT.txt", "w" );
    for ( i=0; i<codeCounter; i++ )
        putc( (codeArray[i].bit)+48, out); // 48:0's ascii code
    fclose(out);
    //codeToAlpha( codeArray, codeCounter );

    ************************************************************
    ************************************************************/
    //bitChange( codeCounter, codeArray, bitmapFile );

    fseek( bmp, 0, SEEK_SET );
    unsigned char header[offset];  // holding header file
    for( i=0; i<offset; i++ )
        header[i] = getc(bmp);

    putSize( header, codeCounter );
    // Copy chenged header for our new bitmap
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
