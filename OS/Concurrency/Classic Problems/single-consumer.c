/*
 * A single-consumer-single-producer program in C
 * Uses conditions to synchronize threads
 * Author : arashTaherK@gmail.com
*/
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <stdio.h>
#include <time.h>

#define CUBBY_SIZE 3    // Cubbyhole size
#define TOTAL_PROD 5   // Total production
#define TRUE 1
#define FALSE 0
#define ABORT() { printf("\nError accured in line "\
        "%d in file %s\n", __LINE__, __FILE__ ); abort(); }

// Cubbyhole is where producer store goods
// Initilized to False
// (Has not been used !)
int cubbyhole[ CUBBY_SIZE ] = {FALSE};
int load = 0;  // Capacity loaded by now
// This parameter has been used as predicate in wait

// Create and initialization of mutex and conditions
pthread_mutex_t mutex   = PTHREAD_MUTEX_INITIALIZER ;
pthread_cond_t notFull  = PTHREAD_COND_INITIALIZER  ;
pthread_cond_t notEmpty = PTHREAD_COND_INITIALIZER  ;

inline void produce() { usleep( rand() % 500000 ); }
inline void consume() { usleep( rand() % 500000 ); }


void *producer( void *args ) {
    int i;
    for ( i=0; i<TOTAL_PROD; i++ ) {
        pthread_mutex_lock( &mutex );

        while ( load == CUBBY_SIZE )
            pthread_cond_wait( &notFull, &mutex );
        
        produce();
        load += 1;
        printf("#%d produced, load : %d\n", i+1, load);

        if ( load == 1 )
            pthread_cond_signal( &notEmpty );

        pthread_mutex_unlock( &mutex );
    }
    return NULL;
}

void *consumer( void *args ) {
    int i;
    for ( i=0; i<TOTAL_PROD; i++ ) {
        pthread_mutex_lock( &mutex );

        // While list is empty wait
        // We use while in here instead of if, because as
        // man page for signal says after each signal more than
        // one thread may wake up. So we use "predicate" to check
        // after we've woken up.
        while( load == 0 )
            pthread_cond_wait( &notEmpty, &mutex );

        consume();
        load -= 1;
        printf("#%d consumed, load : %d\n", i+1, load);

        // A new item has been added to list
        pthread_cond_signal( &notFull );

        pthread_mutex_unlock( &mutex );
    }
    return NULL;
}


int main()
{
    unsigned int iseed = (unsigned int)time(NULL);
    srand( iseed );

    pthread_t produce;
    pthread_t consume;

    if ( pthread_create( &produce, NULL, producer, NULL ) ) ABORT()
    if ( pthread_create( &consume, NULL, consumer, NULL ) ) ABORT()
    
    if ( pthread_join(produce, NULL) ) ABORT();
    if ( pthread_join(consume, NULL) ) ABORT();

    // Clean up
    pthread_mutex_destroy( &mutex   );
    pthread_cond_destroy ( &notFull );
    pthread_cond_destroy ( &notEmpty);

    return 0;
}

