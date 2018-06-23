from threading import Thread
import thread
import chunkReceiver
import random
import auxiliary

class FileReceiver():
    ''' User hase selected a file to download
    In give FileReceiver required info and 
    it will provide us with final file which
    each part of that has been received from
    on peer, so we divide file into number of peers '''

    # TODO : Hashcode instead of file name
    def __init__(self, reqFileName, peers, fileSize):
        #Thread.__init__(self)
        #self.setDaemon(True)
        self.fileName = reqFileName
        self.peers = peers
        self.totalChunks = len(peers)
        print 'TOTAL CHUNK IS :', self.totalChunks
        self.unit = fileSize / self.totalChunks
        # This list will hold whether a chunk has
        # been received properly or not
        self.recvedChunks = [False]*self.totalChunks

    def run(self):
        '''Now we call chunkReceiver for each part'''

        #for i in range( self.totalChunks ) :
            #chunkToPeer[i] = None

        chunkToPeer = {}
        for i in range( len(self.peers) ):
            chunkToPeer[i] = None

        while self.recvedChunks.count(False) != 0 :
            threads = []  # collection of all of our threads
            # which peer send which chunk 
            curChunk = 0
            while curChunk < self.totalChunks :
                if self.recvedChunks[curChunk] == False :
                    print 'LENGTH IS :', curChunk
                    # Which chunk to which peer
                    chunkToPeer[curChunk] = self.peers[ \
                            random.randint(0, len(self.peers)-1) ]
                    threads.append(
                    chunkReceiver.ChunkReceiver( \
                            chunkToPeer[curChunk], \
                            self.fileName, \
                            self.unit*curChunk, \
                            self.unit, \
                            self.recvedChunks )
                    )
                    threads[-1].start()
                curChunk += 1

            # Wait for this threads to finish their job
            for t in threads :
                t.join()

            print 'Recvd is :', self.recvedChunks

            # Check if for a chunk peer could not act well
            # then remove that peer
            #for i in range(len(self.peers)-1,-1,-1) :
            for i in range(len(self.recvedChunks)) :
                print 'I is', i,' and recv :', self.recvedChunks[i]
                if self.recvedChunks[i] == False and \
                        self.peers.count( chunkToPeer[i] ) != 0 :
                    self.peers.remove(chunkToPeer[i])

            print 'now peers are :', self.peers

            if len(self.peers) == 0 :
                #raise RuntimeError, 'There is no peer !'
                print 'There is no other peer !'
                import sys
                sys.exit(0)

        #if False in self.recvedChunks :
            #print 'Something is wrong, try again ...'
        ## TODO :
        ## GO CHECK DOES ANYONE ELSE HAS THE FILE IN HASHCODE ...
        ## ALSO DROP THIS PEER OUT
        ## THIS IS JUST TEST
        #crashedChunks = []
        #for i in self.recvedChunks:
            #if !self.recvedChunks :
                #crashedChunks.append(i)
                #self.peers[i].pop()
        #import random
        #while self.recvedChunks.count(False) != 0 :
            #newPeer = random.randint(0, len(self.peers) )



        #chunkReceiver.ChunkReceiver( \
                #self.peers[self.chunk], \
                #self.fileName, \
                #0, \
                #100*2**10 ).start()
        #chunkReceiver.ChunkReceiver( \
                #self.peers[self.chunk+1], \
                #self.fileName, \
                #100*2**10, \
                #200*2**10 ).start()

def getUserInput():
    comm = True
    while comm :
        comm = raw_input( 'Enter command :' )
        print comm[::-1]

if __name__ == '__main__' :
    FileReceiver( 'a.rar', [('192.168.56.101',50001)], 46345917 ).run()
    #thread.start_new_thread( getUserInput, () )
