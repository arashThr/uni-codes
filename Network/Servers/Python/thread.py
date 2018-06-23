# A simple thread base server
from threading import Thread
import socket

class Server( Thread ):
    "A server to handle muliple user requests"
    def __init__( self, client, addr ):
        # Initialization
        Thread.__init__(self)
        self.setDaemon(True)

        self.c = client
        self.addr = addr

    def run(self):
        self.c.send( 'You have connected to echo server, type ...\n' )
        l = True
        while l :
            l = self.c.recv(1024).strip()
            if l :
                self.c.send( l[::-1] + '\n' )
        self.c.close()

if __name__ == '__main__' :
    sock = socket.socket()
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

    host = ''
    port = 8000

    sock.bind( (host, port) )
    print 'Echo server on port 8000'
    sock.listen(3)

    while True :
        client, addr = sock.accept()
        Server( client, addr ).start()
