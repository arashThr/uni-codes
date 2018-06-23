from socket import *
from threading import Thread
import sys
import time
import auxiliary

#PORT = 50000

class ListenToIP(Thread):
    '''Listen for a broadcast message .
    extarct IP address and file names'''
    def __init__(self):
        Thread.__init__(self)
        # Daemon Threads will terminate when all non-daemons are finished
        self.setDaemon(True)
        # List of all peers and time they've last seen
        self.peers = dict()
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
        # Listen to all interfaces for new packet
        self.s.bind(('', auxiliary.BROADCAST_PORT))
    
    def getPeersIP(self):
        return self.peers.keys()

    def run(self):
        print 'Start listen to IP'
        #print 'My socket name in listen is :', self.s.getsockname()
        while True:
            # Print received data
            data, wherefrom = self.s.recvfrom(1500, 0)
            if wherefrom[0] == auxiliary.myIP :
                continue
            #if auxiliary.peersList.has_key( wherefrom ) :
                #auxiliary.peersList[ wherefrom ] = \
                        #auxiliary.peersList.get( wherefrom ) + data
            #else :
                #auxiliary.peersList[ wherefrom[0] ] = data

            # If it's a new peer or his data have changed
            if not auxiliary.peersList.has_key( wherefrom ) or \
                    auxiliary.peersList[wherefrom] != data :
                auxiliary.peersList[ wherefrom ] = data

            #sys.stderr.write('Received data from : ' + repr(wherefrom) + '\n')
            #sys.stdout.write(data)

            # Set last time seen for this peer
            auxiliary.lastTimeSeen[ wherefrom ] = time.time()

            #for it in self.peers.iterkeys() :
                ## If the peer was silent for more than a minute
                #if time.time()-self.peers[it] > 60 :
                    #peers.pop( it )

