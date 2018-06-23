from Queue import Queue
from Queue import PriorityQueue
from threading import Thread
from time import sleep
from clock import Clock

class IOHandler( Thread ):
    #allRes = [ 'disk', 'network', 'mem', 'intr' ]
    #resources = [ { 'type':allRes[i], 'queue':Queue(), 'isFree':True } 
            #for i in range(len(allRes)) ]
    # New IO request will be placed in here
    # Scheduler fills this one
    IOReqQ = Queue()
    # When an IO request finishes, we will put it here
    # IO devices will fill this one, Scheduler reads it
    IOFinQ = Queue()
    # Create an instance of clock to have access to time
    clk = Clock()

    def __init__( self ):
        Thread.__init__(self)
        self.setDaemon(True)
        # Create and start handlers for each device
        self.disk = Disk()
        self.disk.start()
        self.ram = Ram()
        self.ram.start()
        self.net = Network()
        self.net.start()
        self.intr = Intr()
        self.intr.start()

    def run( self ):
        while True :
            # The process who initiated IO request
            #print 'Waiting for IO request ...'
            proc = IOHandler.IOReqQ.get( True )   # Set blocking true
            #print 'AN IO request received'

            if proc == None :
                'IO is terminating'
                break
            # Extarct required data
            # ( A list of IO infos, second one is type )
            self.ioType = proc.IOInfo[0][1]

            if self.ioType == 'DISK' :
                print IOHandler.clk.repTime(), proc.showPID(), '-> Entered DiskQ'
                Disk.diskQ.put( ( proc.IOInfo[0][0], proc ), True )
            elif self.ioType == 'RAM' :
                print IOHandler.clk.repTime(), proc.showPID(), '-> Entered RamQ'
                Ram.ramQ.put( ( proc.IOInfo[0][0], proc ), True )
            elif self.ioType == 'NETWORK' :
                print IOHandler.clk.repTime(), proc.showPID(), '-> Entered NetQ'
                Network.netQ.put( ( proc.IOInfo[0][0], proc ), True )
            elif self.ioType == 'INTR' :
                print IOHandler.clk.repTime(), proc.showPID(), '-> Entered IntrQ'
                Intr.intrQ.put( ( proc.IOInfo[0][0], proc ), True )
            else :
                raise RuntimeError, 'Unknown IO device'


class Disk( Thread ):
    diskQ = PriorityQueue()
    def __init__( self ):
        Thread.__init__(self)
        self.setDaemon(True)

    def run( self ):
        while True :
            proc = Disk.diskQ.get( True )[1]    # Set blocking true
            print IOHandler.clk.repTime(), proc.showPID(), '-> Start Disk'
            self.priority = proc.IOInfo[0]
            self.ioDuration = proc.bursts[0]

            sleep( proc.bursts[0] )

            print IOHandler.clk.repTime(), proc.showPID(), '-> Finished Disk'
            IOHandler.IOFinQ.put( proc )
            

class Ram( Thread ):
    ramQ = PriorityQueue()
    def __init__( self ):
        Thread.__init__(self)
        self.setDaemon(True)

    def run( self ):
        while True :
            proc = Ram.ramQ.get( True )[1]    # Set blocking true
            print IOHandler.clk.repTime(), proc.showPID(), '-> Start Ram'
            self.priority = proc.IOInfo[0]
            self.ioDuration = proc.bursts[0]

            sleep( proc.bursts[0] )

            print IOHandler.clk.repTime(), proc.showPID(), '-> Finished Ram'
            IOHandler.IOFinQ.put( proc )


class Network( Thread ):
    netQ = PriorityQueue()
    def __init__( self ):
        Thread.__init__(self)
        self.setDaemon(True)

    def run( self ):
        while True :
            proc = Network.netQ.get( True )[1]    # Set blocking true
            print IOHandler.clk.repTime(), proc.showPID(), '-> Start Network'
            self.priority = proc.IOInfo[0]
            self.ioDuration = proc.bursts[0]

            sleep( proc.bursts[0] )

            print IOHandler.clk.repTime(), proc.showPID(), '-> Finished Network'
            IOHandler.IOFinQ.put( proc )


class Intr( Thread ):
    intrQ = PriorityQueue()
    def __init__( self ):
        Thread.__init__(self)
        self.setDaemon(True)

    def run( self ):
        while True :
            proc = Intr.intrQ.get( True )[1]    # Set blocking true
            print IOHandler.clk.repTime(), proc.showPID(), '-> Start Intrrupt'
            self.priority = proc.IOInfo[0]
            self.ioDuration = proc.bursts[0]

            sleep( proc.bursts[0] )

            print IOHandler.clk.repTime(), proc.showPID(), '-> Finished Intrrupt'
            IOHandler.IOFinQ.put( proc )

