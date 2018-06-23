# Some additional function , constant values 
# and some data which need to be shared like peers list

n = [10]
peersList = {} # Each peer and it's files
lastTimeSeen = {} # last time that we have seen a peer
myFileHash = ''
myIP = None # IP of the peer himself
bufSize = 4096
blck_size = 2*20 # For hashing files

BROADCAST_PORT = 50000 # port for UDP connection
DATA_PORT = 50001 # Port for sending and receiving data
PERCENT = 1000

def getFileLen( fin ) :
    # Length of the file
    fin.seek(0, 2)
    fileLen = fin.tell()
    fin.seek(0)
    return fileLen

