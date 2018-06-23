# P2P program
# arashTaherK@gmai.com
# Jan 28, 2012

import socket
from threading import Thread
from broadcastIP import BroadcastIP 
from listen import ListenToIP
import hashlib
import os
import auxiliary
import fileReceiver
import chunkSender
import thread

def createHashes( dirPath ):
    md5 = hashlib.md5()
    blck_size = 2**20 # 1MB each time to update 
    print 'Path is :', os.path.abspath('.'+'/'+dirPath)

    if not os.path.isdir(dirPath):
        raise RuntimeError, 'The given path is incorrect'

    print 'Put files in here to share\n' + \
            'Downloaded files will be in here'

    os.chdir(dirPath)
    # Can be removed
    if len( os.listdir('.') ) > 20 :
        print 'Too many files to share(Just for assurance)'
        raise RuntimeError

    # Hash all files in directory and put them in my_hash_files
    for f in os.listdir('.') :
        print f, 'is hashing ...'
        fin = open(f, 'rb')
        while True :
            data = fin.read( auxiliary.blck_size )
            if not data :
                break
            md5.update( data )

        #print 'Result is : ', repr(md5.hexdigest())
        ## : -> sep between file name and hash
        auxiliary.myFileHash += \
                md5.hexdigest() + ':' + f + ':' + \
                str(auxiliary.getFileLen(fin)) + ' '
        fin.close()

# When we are listing files, we also create a dict
# so later, we can find requested files easier
hash_size = [] # A list contains hash,size tuple of files
hashToFname_peer = {}
# TODO : number of people who own the same file
def listFiles() :
    global hash_size # Initialize the list
    global hashToFname_peer
    hash_size = []
    hashToFname_peer = {}
    i = 1  # counter
    for peerFiles in auxiliary.peersList.iteritems() :
        files = peerFiles[1].split()
        # Print file name and it's size
        for f in files :
            hashCode = f.split(':')[0]
            fileName = f.split(':')[1]
            fileSize = f.split(':')[2]
            print i, ':', fileName, '--->', fileSize
            i += 1
            # ( Hash code, fileSize )
            hash_size.append( (hashCode, fileSize) )
            if not hashToFname_peer.has_key(hashCode) :
                # We want a set of users with this file
                hashToFname_peer[ hashCode ] = list() 
            # Add new file name, peer addr(ip, port) to set
            # Wen need file name because of fileReceiver module
            hashToFname_peer[ hashCode ].append( (fileName, peerFiles[0]) )

        #print 'hash_size :', hash_size
        #print 'hashToFname_peer :', hashToFname_peer

#def downloadFile( selectNo ) :
    #global hash_size
    #global hashToFname_peer
    #index = int(selectNo)-1
    #print 'Index is :', index, 'len is :', len(hash_size)
    #if index >= len(hash_size) :
        #raise IndexError, 'tooooo much'
    #hashCode, fileSize = hash_size[ int(selectNo)-1 ]
    ## Now we have hash code and size of the desired file
    #print 'Hash code :', hashCode
    #print 'File size :', fileSize

    ## Let's find peer swho they have files with this hash code
    #fileNameToPeers = {}
    ##print 'Hash to fanme peer :', hashToFname_peer
    #for fnameToPeer in hashToFname_peer.iteritems() :
        ## We only want to find files related to this hashcode
        #if fnameToPeer[0] != hashCode :
            #continue

        #print 'Fname to peer is :', fnameToPeer
        #fileName = fnameToPeer[1][0][0]
        #peerAddr = fnameToPeer[1][0][1]
        ##print 'File name :', fileName
        ##print 'PeerAddr :', peerAddr
        #if not fileNameToPeers.has_key( fileName ) :
            ## Set of peers who they have this file
            #fileNameToPeers[ fileName ] = set()
        #fileNameToPeers[ fileName ].add( peerAddr )
    #print 'F is :', fileNameToPeers
    ##for f in fileNameToPeers.iteritems() :
        ##print f
    
def downloadFile( select ):
    # Peers for each file name which have the same hachcode
    fileName_peer = {}
    index = int(select)-1
    if index >= len(hash_size) :
        raise IndexError, 'tooooo much'
    hashCode, fileSize = hash_size[ int(selectNo)-1 ]
    print 'Hash code is :', hashCode

    # Search in received data from peers for this hashCode
    for peersFiles in auxiliary.peersList.iteritems() :
        # peer address
        peer = peersFiles[0]
        files = peersFiles[1].split()
        for f in files :
            peerHashCode = f.split(':')[0]
            if peerHashCode == hashCode :
                fileName = f.split(':')[1]
                print 'File with equal is :', fileName
                if not fileName_peer.has_key( fileName ):
                    fileName_peer[ fileName ] = list()
                fileName_peer[ fileName ].append(peer)
                # This peer had this file, let's go for other peers
                break

    print 'Filename_peer :', fileName_peer

    for item in fileName_peer.iteritems() :
        newFileReceiver = fileReceiver.FileReceiver( item[0], item[1], int(fileSize) )
        newFileReceiver.run()


def downloadByName( fname ):
    peersWithFile = []
    fileSize = 0
    for peersFiles in auxiliary.peersList.iteritems() :
        peer = peersFiles[0]
        files = peersFiles[1].split()
        for f in files :
            fileName = f.split(':')[1]
            if fileName == fname :
                fileSize = f.split(':')[2]
                peersWithFile.append( peer )
                break
    print 'Peers who have the file :', peersWithFile
    if len(peersWithFile) != 0 :
        newFileReceiver = fileReceiver.FileReceiver( fname, peersWithFile, int(fileSize) )
        newFileReceiver.run()



# TODO : IPAddress = raw_input('Enter your IP address :')
#bip = BroadcastIP('192.168.56.1')
#bip.start()
#lis = ListenToIP()
#lis.start()
#import time
#while True :
    #print 'Peers are :', lis.getPeersIP()
    #time.sleep(3)

# Start to listen to other peers in another thread
lis = ListenToIP()
lis.start()

# Start chunk sender server
#thread.start_new_thread( chunkSender.server(), () )
chunkSenderServer = chunkSender.chunkServer()
chunkSenderServer.start()

# TODO : dirPath
#dirPath = raw_input('Enter dir name and wait for init : ')

# Start hashing files
createHashes( 'Files' )
#print 'Now hashes are :', auxiliary.myFileHash

auxiliary.myIP = raw_input('Enter your IP :')
bip = BroadcastIP(auxiliary.myIP)
bip.start()

comm = True 
while comm != 'exit' :
    comm = raw_input('"ls","dlh", "dln", "exit" : ')
    if comm == 'ls' :
        listFiles()
    elif comm == 'dlh' :
        listFiles()
        selectNo = raw_input('Select number : ')
        downloadFile(selectNo)
    elif comm == 'dln' :
        fname = raw_input('Enter file name : ')
        downloadByName(fname)
