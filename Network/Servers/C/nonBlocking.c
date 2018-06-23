/* This is a simple echo server which uses
   fcntl to make a blocking funtion call on
   receiving data from client to a nonblocking
   then, after a interval, we can checke resources again
*/
#include<sys/socket.h>
#include<arpa/inet.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h> // closing the sockets
#include<sys/sendfile.h>
#include<fcntl.h>
#include<memory.h>

#define MAX_CLIENTS 10
#define BUF_LEN 64
#define True 1
#define False 0
#define PORT_ADDR 8000
#define BACKLOG 5
#define DELAY 1
/* The sequence of our system call for server would be :
 * Socket()
 * Bind()
 * Listen()
 * Accept()
 */

struct client_data {
    int sockfd;
    struct sockaddr_in client_addr;
};

void *handle_req( void * );   /* thread function to handle multiple connections */
void *comm_line( void *);   /* thread to receive server side commands */
void dump_line( FILE * );   /* dump remaining chars on current input line of a file */

int main ( int argc , char ** argv )
{
	int sockfd ; // Listen on sockfd, Socket file descriptor

	struct sockaddr_in my_addr ; // Internet socket address
	struct sockaddr_in their_addr ; // Specifications of who requests
	socklen_t sin_size = sizeof( my_addr );

	sockfd = socket( AF_INET, SOCK_STREAM, 0 ); //domain, type, protocol(zero means auto)
	int optval = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof optval);
	
    // Initializing new socket
    my_addr.sin_family = AF_INET; // Int socket family, addres format
	my_addr.sin_port = htons( PORT_ADDR ) ; // host to network short ( little endian to big endian )
	my_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	//inet_aton( "127.0.0.1", &(my_addr.sin_addr) );
    bzero( &my_addr.sin_zero, 8 );

	// Binding, for listener
	bind( sockfd, (struct sockaddr *)&my_addr, sin_size ); // Let us listen to a specific port
    // Listen to the port and accept connections
	printf("IP addr is : %s\n", inet_ntoa( my_addr.sin_addr) ); 
    printf("Listening on port : %d\n", PORT_ADDR);
    /*printf("Port is : %d\n", my_addr.sin_port ); */
	listen( sockfd, BACKLOG );

    // Accept
    int counter = 0 ;
    char *msg = "Welcome user to ECHO server\n";
    char buf[BUF_LEN];
    int new_fd[MAX_CLIENTS] ; // New connection would be accepted on new_fd
    int init ;
    /*memset( new_fd, -1, MAX_CLIENTS );*/
    for ( init=0; init<MAX_CLIENTS; init++ )
        new_fd[init] = -1;

    fcntl( sockfd, F_SETFL, O_NONBLOCK );   // Nonblocking for accept
	while ( True ) {
        int i;
        for ( i=0; i<MAX_CLIENTS; i++ )
            if ( new_fd[i] == -1 ) {
                counter = i;
                break;
            }
        if( i==MAX_CLIENTS ) {
            printf("We have reached the max number of clients\n");
            exit(1);
        }
        if ( (new_fd[counter] = \
                accept( sockfd, (struct sockaddr *)&their_addr\
                , &sin_size ) ) != -1 ) { 
            printf("Got connection from : %s\n", inet_ntoa( their_addr.sin_addr) );
            fcntl( new_fd[counter], F_SETFL, O_NONBLOCK );      // Now new_fd is nonblocking

            // Send welcome message
            int sent_bytes = send( new_fd[counter], msg, strlen(msg), 0 );
            if ( sent_bytes == -1 ) {
                puts("Error occured while sending");
                exit(1);
            }
        }

        int checke;
        for( checke=0; checke<counter; checke++ ) {
            int recvd_data = recv( new_fd[checke], buf, sizeof(buf), 0 );
            /*printf("Recevd was : %d\n", recvd_data);*/
            if ( recvd_data == -1 ) // Nothing to read
                continue ;
            if ( recvd_data == 0 ) {    // Connection closed
                printf( "User %s disconnected\n", inet_ntoa( their_addr.sin_addr) );
                new_fd[checke] = -1;
                continue ;
            }
            buf[recvd_data] = '\0' ;
            int bytes_written = send(new_fd[checke], buf, strlen(buf), 0);
            if (bytes_written <= 0) {
                puts("Can not send all bytes !"); 
                exit(1);
            }
        }
        sleep(DELAY);   // Sleep for DELAY second and then checke resources
	}
	close(sockfd);

    return 0;
}

