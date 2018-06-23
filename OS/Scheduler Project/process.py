from time import sleep
from algorithm import Algorithm

class Process :
    pid = 1
    def __init__( self, attrs ):
        self.procInfo = {}
        self.procInfo['pid'] = Process.pid
        self.procInfo['mem'] = float(attrs[1])     # Mem usage
        self.procInfo['start'] = float(attrs[0])   # Start time
        self.procInfo['hasStarted'] = False    # Has process started
        self.procInfo['finTime'] = -1   # When does the process finished
        # This will be evaluated later, in bursts
        self.procInfo['noOfEvents'] = 0
        # States are : NEW, RUNNING, WAITING and FINISHED
        # TODO : Can be used in preemptive algorithm to detect new processes
        self.procInfo['state'] = 'NEW'
        # Process execution time by now
        self.procInfo['totalExecTime'] = 0
        # last CPU burst duration
        self.procInfo['lastExecTime'] = Algorithm.EXEC_DEF
        # Tickets used in lottery algorithm
        self.tickets = []
        # Level of execution for current processin MLFQ
        self.procInfo['level'] = 1
        # Execution time calculated by burstes
        self.totalBursts = 0
        # Sequence of bursts, to calculate totalExectime
        self.burstSeq = []

        Process.pid += 1
        # This will be a list of bursts
        # Sequence is : CPU, IO, CPU, IO, ...
        self.bursts = []
        # This will hold a list of info about each IO burst
        # [ [Prio, Type], ... ]
        self.IOInfo = []
        # Two types of bursts : CPU and IO
        # First one is always CPU
        self.curBurst = 'CPU'

    def addBurst( self, duration ):
        self.bursts.append( float(duration) )
        if self.procInfo['noOfEvents'] % 2 == 0 :
            self.totalBursts += float(duration)
            self.burstSeq.append( float(duration) )
        self.procInfo['noOfEvents'] += 1

    def AddIOInfo( self, attrs ):
        # Type and priority of an IO
        self.IOInfo.append( [ int(attrs[0]), str(attrs[1]) ] )

    def runProc( self, interval ):
        '''Run a process by decreminting it's requires time and
        return final state : another cpu req, io req or finished'''

        self.procInfo[ 'state' ] = 'RUNNING'
        # Decrement time

        #print 'Burst :', self.bursts[0], 'int :', interval

        if self.bursts[0] <= interval :
            # This burst has been finished ( remove )
            # Update process time info
            self.bursts.pop(0)
            self.procInfo['totalExecTime'] += self.procInfo['lastExecTime']
            self.procInfo['lastExecTime'] = self.burstSeq.pop(0)
            #print 'Poped, next is :', self.bursts[0]
            self.procInfo['noOfEvents'] -= 1
            #print 'Events :', self.procInfo['noOfEvents']
            if self.curBurst == 'IO' :
                self.curBurst = 'CPU'
            else :
                self.curBurst = 'IO'
        else :
            self.bursts[0] -= interval
        
        # Set new state
        if self.procInfo[ 'noOfEvents' ] == 0 :
            self.procInfo[ 'state' ] = 'FINISHED'     # Process finished
        elif self.curBurst == 'IO' :
            self.procInfo[ 'state' ] = 'WAITING'    # IO request
        else :
            self.procInfo[ 'state' ] = 'READY'

    # Define cmp for priority queue for IO requests
    #def __cmp__( self, other ) :
        #print 'Type self :', type(self)
        #print 'Type other :', type(other)
        #return cmp( self.IOInfo[0][0], other.IOInfo[0][0] )

    def showPID( self ):
        return 'Process ' + str( self.procInfo['pid'] ).zfill(3)

    def showProcInfo( self ):
        print 'PID :', self.procInfo['pid']
        print 'Start :',self.procInfo['start'],
        print ', Mem :',self.procInfo['mem'],
        print ', Events :', self.procInfo['noOfEvents']
        print 'Bursts are :', self.bursts
        print 'IO :', self.IOInfo


