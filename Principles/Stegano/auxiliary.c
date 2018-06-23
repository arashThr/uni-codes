#include"Header.h"

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

int getLine( char *str, int len )  // get line from the input
{
    int i ;  // The length of input
    char c ;

    for ( i=0; i<len-1 && ( c=getchar() ) != '\n'; i++ )
        str[i] = c ;
    str[i] = '\0' ;

    if ( !strcmp(str,"0") )
        return 0 ;

    return i;
}

void getPicInfo( char *bitmapFileName )
{
    int i ;
    FILE *bmp = fopen( bitmapFileName, "rb" );
    if ( !bmp ) {
        printf( "Can not open Picture file addressed : %s\n", bitmapFileName );
        printf( "Check : 1) Existence of addressed picture\n" \
                "2) Make sure your picture color depth is 24 bit/pixel\n");
        return ; // 2
    }

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
    if ( codeSize == 0 )
        printf ( "The Picture is a normal picture ( not coded )\n" );
    else
        printf ( "Picture is coded\n" \
                  "Size of coded information is : %d kb\n", codeSize/8000 );

    printf("Max text capacity to hide : %d kb\n", (((size-offset)*2)/8)/1000);
    printf("Picture size              : %d kb\n", size/1000  );
    printf("Color depth               : %d bit/pixel\n", BpP );
}

void wait ( int seconds )
{
  clock_t endwait;
  endwait = clock () + seconds * CLOCKS_PER_SEC ;
  while (clock() < endwait) {}
}

void help()
{
    printf("\nWelcome to Steganography program\n" \
           "By using this program you can store your information in an ordinary picture\n" \
           "And retrive them later\n" \
           "You can be sure that difference between coded program and your simple picture\n" \
           "is such little that maby you can't remember that it was a coded picture or not\n" \
           "Just make sure : \n" \
           "1) You are using a 24bit/pixel Bitmap picture\n" \
           "2) You have permission to read and write in folder that you want to do operation on it\n\n" \
           "If you had any kind of problem with this program or you have found some bugs\n" \
           "You can send me E-mail to address : \n" \
           "\"arashTaherK@gmail.com\"\n"
           "Goodbye and good luck\n\n" );
}
