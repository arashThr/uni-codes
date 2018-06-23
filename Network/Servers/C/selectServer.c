// A simple echo server using "Select"

#include<sys/socket.h>
#include<time.h>
#include<sys/types.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/sendfile.h>

/* The sequence of our system call for server would be :
 * Socket()
 * Bind()
 * Listen()
 * Accept()
 */

#define BACKLOG 5 // How many pending connection queue will hold
#define PORT_ADDR 8000

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

    // Let's create a thread to accept command in server sind

    // Accept
    // First let's initialize prereq's for select
    /*struct timeval tv ;*/ // Our server will serve forever
    fd_set readfds ;
    fd_set master ; // Select actually changes the set you pass into it
    FD_ZERO( &readfds );    // Clear all entries from the set
    FD_ZERO( &master );
    /*FD_SET( 0, &master );  // stdin*/
    FD_SET( sockfd, &master ); // Checke this fd for new connections

    int max_fd ; 
    max_fd = sockfd ; // We need this value for select
    int fd; // Loop over all fd's in master(readfds)

    for(;;) {
        // Wait for : 1.new requesr 2.input 3.data from a client
        readfds = master ;  // Copying ( select manipulates it's argument )
        if ( select( max_fd+1, &readfds, NULL, NULL, NULL ) == -1 ) {
            perror( "Select error occured !" );
            exit(1);
        }

        for ( fd=3; fd<max_fd+1; fd++ )
        {
            // Request for establishing new connection
            if ( FD_ISSET( fd, &readfds ) && fd == sockfd) {
                // New connection will be accepted on new_fd
                int new_fd = accept( fd, (struct sockaddr *)&their_addr, &sin_size );
                if ( new_fd == -1 )
                    perror( "Error:31" );
                else {
                    printf("Got connection from : %s\n", inet_ntoa( their_addr.sin_addr) );
                    char *msg = "Welcome user to ECHO server\n";
                    int sent_bytes = send( new_fd, msg, strlen(msg), 0 );

                    if ( sent_bytes == -1 ) {
                        puts("Error occured while sending");
                        exit(1);
                    }

                    FD_SET( new_fd, &master );
                    // Set new value for max_fd
                    if ( max_fd < new_fd )
                        max_fd = new_fd ;
                }
                /*break;*/
            }

            // New peice of data has been received from a client
            else if( FD_ISSET( fd, &readfds ) ) {
                char buf[BUFSIZ];  
                int recvd_data = recv( fd, buf, sizeof(buf), 0 );
                buf[recvd_data] = '\0' ;
                
                // data received , now let's do echo
                if ( recvd_data > 0 ) {
                    /*printf("Users says : %s\n", buf);*/
                    int bytes_written = send(fd, buf, strlen(buf), 0);
                    if (bytes_written < 0) {
                        puts("Can not send all bytes !"); 
                        exit(2);
                    }
                }
                else if ( recvd_data <= 0 ) {    // Connection closed
                    printf( "User %s disconnected\n", inet_ntoa( their_addr.sin_addr) );
                    if ( recvd_data < 0 )
                        perror( "Error" );
                    FD_CLR( fd, &master );
                    close( fd );
                }

                /*break;  // We have nothing else to do here*/
            }
        }
    }
	close(sockfd);

    return 0;
}

// If you want to use command line also, all you have to do
// is to FD_SET( 0, &master ) : add stdin and handle it
void *comm_line( void *args )
{
    puts( "You use specific commands like : exit, say\n" );
    char comm[8] = "";
    while ( strcmp( comm, "exit\n" ) ) {
        fgets( comm, sizeof(comm), stdin );
        printf("Comm is : %s\n", comm);
        puts("sdfas");
        if ( !strcmp( comm, "say\n" ) )
            puts("Hello dear :)");
        else
            puts("StOp tYpINg NonSeNsE X(");
    }
    exit(0);
}

