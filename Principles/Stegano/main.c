/******************** Steganography ***********************
*** Arash Taher *******************************************
*** 2010 AD   *********************************************
*** arashTaherK@gmail.com *********************************
*** Shiraz Univesity **************************************
*** 882980 ************************************************
***********************************************************/

#include"Header.h"

int main()
{
    char c ;
    char *fileLoc = (char *)malloc( PATH_SIZE );
    char *picLoc  = (char *)malloc( PATH_SIZE );

    printf( "**************** Steganography ****************\n" \
            "***********************************************\n" \
            "****** Hide Your Information In A Picture *****\n" \
            "*********** And Retrive Them Later ************\n" \
            "***********************************************\n");
    do {
        printf( "\n"                                    \
                "1) \"S\"tegano a Picture\n"            \
                "2) \"D\"eStegano a Picture\n"          \
                "3) \"G\"et Picture Information\n"      \
                "4) \"H\"elp\n"                         \
                "5) \"Q\"uit\n"                         \
                "0) \"0\" go to previous step\n" \
                "Press : "                                );
        c = getche() ;
        printf("\n\n") ;
        c = toupper(c);

        switch (c) {
            case 'S' :
                L1:printf( "Enter -> Bitmap file location : " );
                if ( !getLine(picLoc, PATH_SIZE) )
                    break;
                printf( "Enter -> Text file location   : " );
                if ( !getLine(fileLoc, PATH_SIZE) )
                    goto L1 ;
                printf("\n");

                stegano( fileLoc, picLoc );
                break ;

            case 'D' :
                printf( "Enter -> Bitmap coded file location : " );
                if ( !getLine( picLoc, PATH_SIZE ) )
                    break ;
                printf("\n");

                deStagano( picLoc );
                break ;

            case 'G' :
                printf( "Enter -> Bitmap file location : " );
                if ( !getLine( picLoc, PATH_SIZE ) )
                    break ;
                printf("\n");

                getPicInfo( picLoc );
                break ;

            case 'H' :
                help();
                break;

            case 'Q' :
                printf ("\nWe hope you've been enjoyed of using this program :)\n");
                break ;

            default :
                printf("Press one \"S , D , G , H , Q\" button\n\n\a");

        }

    } while( c != 'Q') ;

    free( picLoc );
    free( fileLoc);

    return 0;
}
