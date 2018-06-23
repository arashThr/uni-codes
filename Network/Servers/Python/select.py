# A simple select base server
import socket
import select
import sys

if __name__ == '__main__' :
    sock = socket.socket()
    sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )

    host = ''
    port = 8000

    sock.bind( (host, port) )
    print 'Bound to port 8000 on localhost'
    print 'Enter exit to terminate server'
    sock.listen(3)

    inputs = [ sock, sys.stdin ]

    while True :
        rs, ws, es = select.select( inputs, [], [] )
        for r in rs :
            # A new request established
            if r is sock :
                c, addr = sock.accept()
                print 'Got connection from :', addr
                inputs.append( c )

            # A command has been typed
            elif r is sys.stdin :
                line = sys.stdin.readline().strip()
                print line
                if line == 'exit' :
                        exit();

            # Echo reverse message for client
            else :
                try :
                    data = r.recv(1024).strip()
                    disc = False
                except socket.error() :
                    data = True

                if disc or not data :
                    print 'Peers %s disconnected' % repr(addr)
                    r.close()
                    inputs.remove(r)

                else :
                    r.send( data[::-1] + '\n' )

