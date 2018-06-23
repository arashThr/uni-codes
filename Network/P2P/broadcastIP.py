# Broadcast IP address each 3 seconds
from socket import *
from threading import Thread
import time
import os
import auxiliary

#PORT = 50000
#IP_ADDR = '192.168.56.1'
#IP_ADDR = ''

class BroadcastIP(Thread):
    '''This class will broacast IP, Files and their
    hash code of this peer in exact periods of time.'''
    def __init__(self, IPAddr) :
        print 'Start of broadcast'
        Thread.__init__(self)
        self.setDaemon(True)
        # Holds peers and the last they've been seen
        peersIP = dict()
        # Create a UDP socket for broadcasting
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
        # Theres's no need to bind
        self.s.bind( (IPAddr, auxiliary.BROADCAST_PORT) )
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    
    def run(self) :

        #avail_files = ''
        #file_list = os.listdir('Files')
        #for f in file_list :
            ## TODO : File size and Hash code
            #avail_files += f

        while True :
            # Now sends it files info to other peers
            data = auxiliary.myFileHash # + '\n'
            # Broadcast IP and files
            self.s.sendto(data, \
                    ('<broadcast>', auxiliary.BROADCAST_PORT))

            # Now check peers for time out
            for lastTime in auxiliary.lastTimeSeen.iteritems() :
                if lastTime[1] != -1 and \
                        time.time()-lastTime[1] > 10 :
                    print lastTime[0], 'is gone'
                    auxiliary.peersList.pop( lastTime[0] )
                    auxiliary.lastTimeSeen[lastTime[0]] = -1

            time.sleep(3)

