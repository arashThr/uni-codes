# A simple socket server which take advantages
# of socketServer library to establish a
# multi-threaded server

import SocketServer

class Handler( SocketServer.StreamRequestHandler ):

    def handle(self) :
        self.wfile.write("Welcome to echo server ...\n")
        line = True
        while line :
            line = self.rfile.readline().strip()
            if line :
                self.wfile.write( line[::-1] + '\n' )

if __name__ == '__main__' :
    print 'Server established on port 8000'
    server = SocketServer.ThreadingTCPServer( ('', 8000), Handler )
    server.serve_forever()
