import socket
from threading import Thread
import os
from sys import stdout
import auxiliary

PORT = 50001 # can be imported from auxiliry file

class ChunkReceiver(Thread):
    ''' We have located a file in our network
    and all the peers who they have this file .
    Now we send request to each peer for a certain
    part of our file and gather them togather .
    At the end ChunksReciever will gives us the reqFile'''

    # TODO : address of the peer
    def __init__(self, peerAddr, reqFileName, \
            startAddr, unitSize, recvedChunks ):
        ''' Open socket to a peer, open output file
        Start to revieve file at the given start address '''
        Thread.__init__(self)
        
        # recvedChunk : to check the whether 
        # our job is done or not
        self.recvedChunks = recvedChunks
        # IMP : We should not set setDaemon
        # becuase temination of program will terminate thread
        #self.setDaemon(True)

        self.startAddr = startAddr
        self.unitSize = unitSize
        self.peerAddr = ( peerAddr[0], auxiliary.DATA_PORT )
        # Requested file
        self.fileName = reqFileName

        self.sock = socket.socket()
        print 'Address to connect :', str(self.peerAddr)
        self.sock.connect( self.peerAddr )
        # Open output file
        # ! copy should be removed
        if os.path.exists("copy"+reqFileName) :
            # Already we have recieved some parts
            self.fout = open("copy"+reqFileName, 'r+b')
        else :
            self.fout = open("copy"+reqFileName, 'wb' )
        # Seek to start of that chunk
        self.fout.seek( startAddr )

        # TODO TODO TODO : CAN TOW THREADS HAVE ACCESS TO SAME
        # FILE AT THE SAME TIME ???

    def run(self):
        print 'At chunkSend run'
        # NOW send your request
        # Req consisted of tow parts :
        # hash code, chunk number
        # ( Due to security reasons we don't send file names :P )
        # TODO : change name to hash code
        self.sock.sendall( \
                self.fileName+ ' ' + \
                str(self.startAddr)+ ' ' + \
                str(self.unitSize) + '\r\n' )
        print 'After sending data, befor recv'
        totalSize = 0
        counter = 0
        print 'Unit :', self.unitSize
        while True :
            counter += 1
            if counter%auxiliary.PERCENT == 0 :
                #stdout.write('\r%.2f%% received from %s' % ( \
                        #float(totalSize) / self.unitSize, \
                        #str(self.peerAddr) ) )
                #stdout.flush()
                print '%.2f%% received from %s' % ( \
                        float(totalSize) / self.unitSize, \
                        str(self.peerAddr) )
                counter = 0

            rcvd = self.sock.recv( 4096 )
            totalSize += len(rcvd)
            if not rcvd :
                break
            self.fout.write( rcvd )

        #data = self.sock.recv( 1024 )
        #print 'After recv'
        #while data :
            #print 'Server says :', data
            #data = self.sock.recv( 1024 )

        print '\nTotal revcd size is :', totalSize
        if totalSize == self.unitSize :
            print 'YESSSSSSSSSSSSSSSSSSSSSSSSS'
            self.recvedChunks \
                    [ self.startAddr/self.unitSize ] = True
        else :
            print 'NOOOOOOOOOOOOOOOOOOOO'
            self.recvedChunks \
                    [ self.startAddr/self.unitSize ] = False
        #self.fout.write('hello')

        self.fout.flush()
        self.fout.close()
        self.sock.close()

