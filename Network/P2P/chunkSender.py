#from SocketServer import TCPServer, StreamRequestHandler, ThreadingMixIn
import os
import SocketServer
from threading import Thread
import thread
from socket import *
import time
import auxiliary

#class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer): pass

class chunkServer(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)

        self.s = socket(AF_INET, SOCK_STREAM )
        self.s.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
        self.s.bind(('', auxiliary.DATA_PORT))

    def run(self):
        self.s.listen(5)
        while True :
            c, addr = self.s.accept()
            #addr = self.request.getpeername()
            print 'Got connection from :', addr
            # Read clients request
            msg = c.recv(1024)
            #print 'client says :', msg
            #self.wfile.write('hi dudu !!!')

            print 'Client says :', msg
            # Structure of a msg : hashCode(FileName) +
            # start addr + chunk size
            msg = msg.split(' ')
            reqFileName = msg[0]
            startAddr = msg[1]
            unitSize = msg[2]
            if os.path.exists(reqFileName):
                freq = open( reqFileName, 'rb' )
            else : # i should send a msg to tell client this file does not exist
                raise IOExecption
            # Send response to client
            freq.seek( int(startAddr) )
            c.sendall( freq.read( int(unitSize) ) )

            #time.sleep(5)
            #self.wfile.write('Thank you again man :)\n')
            c.close()

#def server() :
    #server = Server( ('', auxiliary.DATA_PORT), Handler )
    #server.serve_forever()

if __name__ == '__main__' :
    print 'In main'
    #thread.start_new_thread( server, () )
    #server()
    newSender = chunkServer()
    newSender.start()
