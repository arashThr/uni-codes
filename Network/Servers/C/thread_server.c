/* In here we have implemented a simple echo server with
   capability of handling more than one connection at a time.
   To aquire this functionality we took advantage of 
   "Pthread" library
*/

#include<sys/socket.h>
#include<arpa/inet.h>
#include<string.h>
#include<stdio.h>
#include<stdlib.h>
#include<unistd.h> // closing the sockets
#include<sys/sendfile.h>
#include<pthread.h>

/* The sequence of our system call for server would be :
 * Socket()
 * Bind()
 * Listen()
 * Accept()
 */

#define BACKLOG 5 // How many pending connection queue will hold
#define PORT_ADDR 8000

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

    // Let's create a thread to accept command in server sind
    pthread_t comm ;
    if( pthread_create( &comm, NULL, comm_line, NULL ) ) {
        perror( "Can not create command line thread\n" );
        exit(1);
    }

    // Accept
	while ( 1 ) {
        int new_fd ; // New connection would be accepted on new_fd
        new_fd = accept( sockfd, (struct sockaddr *)&their_addr, &sin_size );
        struct client_data *new_user = NULL ;
        if ( (new_user = malloc( sizeof(struct client_data) ) ) == NULL ){
            perror( "Can not allocate resources\n");
            exit(1);
        }
        new_user->sockfd = new_fd;
        new_user->client_addr = their_addr;

        // For each new connection we create a new thread
        pthread_t thr;
        if ( pthread_create( &thr, NULL, handle_req, new_user ) ) {
            perror( "Could not answer to new client" );
            exit(1);
        }
	}
	close(sockfd);

    return 0;
}

// Serve the client with desired file
void *handle_req( void *user_data ) 
{
    int new_fd = ((struct client_data *)user_data)->sockfd ;
    struct sockaddr_in client = ((struct client_data *)user_data)->client_addr ;

    printf("Got connection from : %s\n", inet_ntoa( client.sin_addr) );

    char *msg = "Welcome user to ECHO server\n";
    int sent_bytes = send( new_fd, msg, strlen(msg), 0 );
    if ( sent_bytes == -1 ) {
        puts("Error occured while sending");
        exit(1);
    }

    char buf[64];  
    int recvd_data = recv( new_fd, buf, sizeof(buf), 0 );
    buf[recvd_data] = '\0' ;
    // data received , now let's do echo
    while ( recvd_data > 0 ) {
        /*printf("Users says : %s\n", buf);*/
        int bytes_written = send(new_fd, buf, strlen(buf), 0);
        if (bytes_written <= 0) {
            puts("Can not send all bytes !"); 
            exit(1);
        }
        printf("Written data : %d\n", bytes_written);

        // Receive new chunk of data
        recvd_data = recv( new_fd, buf, sizeof(buf), 0 );
        buf[recvd_data] = '\0' ;
    }

    printf( "User %s disconnected\n", inet_ntoa( client.sin_addr) );

    close(new_fd); 

    return NULL;   
}

void *comm_line( void *args )
{
    puts( "Acceptable commands : exit, say" );
    char comm[8] = "";
    while ( strcmp( comm, "exit\n" ) ) {
        fgets( comm, sizeof(comm), stdin );
        printf("Comm is : %s", comm);
        if ( !strcmp( comm, "say\n" ) )
            puts("Hey Dude :)");
        else if (strcmp( comm, "exit\n" ) )
            puts("Stop typing nonsense >:(");
    }
    exit(0);
}

// Reads and dump any remaning char on the current inpute
// line of a file
void dump_line( FILE *fp ) {
    int ch=0;
    while ( (ch==fgetc(fp)) != EOF && ch != '\n' );
}
