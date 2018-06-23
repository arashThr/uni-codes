# Main scheduling handler
# arashTaherK@gmail.com
from Queue import Queue
from clock import Clock
from random import randint

class Algorithm :
    # Current runing process pid
    curProc = -1
    algSelected = False
    # Alpha value used in SPN algorithm
    ALPHA = .5
    # S1 in formula used for SPN as default execetion value
    # Sn+1 = a Tn + (1-a) Sn
    EXEC_DEF = 3
    # Choosen algorithm is preemptive or not
    isPreemptive = True
    # Total number of tickets that can be assigned
    totalTickets = 100
    # Tickets which we can assign to processes
    tickets = [ i for i in range(totalTickets) ]
    assignedTickets = []

    # Queue for RR algorithm
    RRQ = Queue()

    def __init__( self ):
        # for each new alg activated we will enter a new record
        self.algs = {}
        self.curAlgName = None
        self.startTime = 0
        self.qt = 0

    # Activate new alg and init it
    # Called from readInput while parsing input
    def activateAlg( self, name, attrs ) :
        # attr[0] is start, [1] is qt
        # these are unicode, to use need to be changed to int
        self.algs[name] = attrs[0]
        self.algs[name].reverse()

    # Based on activated algs and their start time we switch
    # between algorithms
    def selectAlg( self, clk ):
        '''In here we search to see if we should switch algorithm'''
        curTime = clk.getTime()
        for alg in self.algs :
            # Start time of 'alg' algorithm
            time = float(self.algs[alg][0])
            if time <= curTime and time > self.startTime :
                print clk.repTime(), 'Algorithm %s is in use' % alg
                self.startTime = time
                self.curAlgName = alg
                if alg == 'RR' or alg == 'LOTTERY' or alg == 'MLFQ' :
                    self.qt = float(self.algs[alg][1])
                if alg == 'FCFS' or alg == 'HRRN' or alg == 'SPN' :
                    Algorithm.isPreemptive = False
                Algorithm.algSelected = True
        #print 'SELF.start =', self.startTime

    # Which process to run, among processes list
    def chooseProc( self, procs, clk ):
        '''Gets list of processes in ready list,
        choose one of them based on slected algorithm'''
        if self.curAlgName == 'FCFS' :
            return FCFS( procs )
        elif self.curAlgName == 'SPN' :
            return SPN( procs )
        elif self.curAlgName == 'RR' :
            return RR( self.qt, procs )
        elif self.curAlgName == 'SRTF' :
            return SRTF( procs )
        elif self.curAlgName == 'HRRN' :
            return HRRN( procs, clk )
        elif self.curAlgName == 'LOTTERY' :
            return lottery( self.qt, procs )
        elif self.curAlgName == 'MLFQ' :
            return MLFQ( self.qt, procs )
        else :
            raise RuntimeError, 'unkown algorithm'

    def showAlgs( self ):
        print 'Algorithms are :'
        for alg in self.algs :
            print alg, self.algs[alg]


# Algorithms implementaion
# Input : list of currently ready processes
# Output : Next process to run ( None, if there isn't any )

# First-come-first-served on ready processes
def FCFS( procs ) :
    #print 'FCFS is using'
    # Next process to run is the one First Came
    #if len(procs) == 0 :
        #raise RuntimeError, 'No process to schedule : 143'
    if len( procs ) == 0 :
        return None

    minStart = procs[0].procInfo['start']
    nxt = None  # next process to run
    for p in procs :
        if p.procInfo[ 'start' ] <= minStart :
            nxt, minStart = p, p.procInfo[ 'start' ]

    # nxt = None if no process has been found
    return nxt


# Several clock will shape a qt
qtFraction = 0
# During these clocks we should run the same process
curProcIndex = -1
prevLen = -1
def RR( qt, readyQ ):
    global qtFraction, curProcIndex, prevLen
    #print 'LEN IS :', len(readyQ)

    # runProc takes care of when process has finished
    # In here we should be careful about qt

    # A little bit tricky !
    # If our process has been finished in it's qt
    # We should choose another process and give it time
    if prevLen != len( readyQ ) :
        prevLen = len( readyQ )
        curProcIndex = curProcIndex % len(readyQ)
        qtFraction = 0

    if len( readyQ ) == 0 :
        return None

    if qtFraction >= qt :
        qtFraction = 0
        
    if qtFraction == 0 :
        qtFraction += Clock.INTERVAL
        curProcIndex = (curProcIndex+1) % len(readyQ)
        return readyQ[ curProcIndex ]

    if qtFraction < qt :
        #print 'Index :', curProcIndex
        #print 'STAT :', readyQ[curProcIndex].procInfo['state']
        qtFraction += Clock.INTERVAL
        return readyQ[ curProcIndex ]


# SRTF algorithm
# As input, gets a list of ready to run processes
def SRTF( procs ):
    if len( procs ) == 0:
        return None

    minRT = procs[0]
    for p in procs :
        #print 'Process :', p.procInfo['pid'], p.bursts[0], '--', minRT.bursts[0]
        if minRT.bursts[0] > p.bursts[0] :
            minRT = p

    return minRT


def SPN( procs ):
    if len( procs ) == 0 :
        return None

    nxtProc = None  # next process to run
    alpha = Algorithm.ALPHA
    minPredict = -1
    for p in procs :
        prediction = alpha*p.procInfo['lastExecTime'] + \
                (1-alpha)*p.procInfo['totalExecTime']
        if minPredict == -1 or prediction < minPredict :
            minPredict = prediction
            nxtProc = p

    return nxtProc

def HRRN( procs, clk ):
    nxtProc = None  # next process to run
    alpha = Algorithm.ALPHA
    respRatio = -1
    for p in procs :
        prediction = alpha*p.procInfo['lastExecTime'] + \
                (1-alpha)*p.procInfo['totalExecTime']
        waitingTime = clk.getTime() - p.procInfo['start']
        rr = ( waitingTime + prediction ) / prediction
        if respRatio == -1 or rr < respRatio :
            nxtProc = p
            rr = respRatio

    return nxtProc


lotQtFraction = 0
lotCurProc = None
def lottery( qt, procs ):
    global lotQtFraction, lotCurProc

    # In this two situation we have to pick new process
    #if len( Algorithm.assignedTickets ) < 1 :
        #return None

    if lotCurProc == None or lotQtFraction >= qt or \
            lotCurProc.procInfo['finTime'] != -1 or \
            lotCurProc.procInfo['state'] != 'READY' :
        lotQtFraction = 0
        randIndex = randint( 0, len( Algorithm.assignedTickets )-1 )
        ticket = Algorithm.assignedTickets[randIndex]

        for p in procs :
            if ticket in p.tickets :
                lotCurProc = p
                break

    lotQtFraction += Clock.INTERVAL
    return lotCurProc


mQtFraction = 0
mUpperBound = 0
mCurProc = None
def MLFQ( qt, procs ):
    global mQtFraction, mCurProc, mUpperBound

    if mCurProc == None :
        mCurProc = procs[0]
        mUpperBound = qt
        return mCurProc

    if mCurProc.procInfo['level'] == 3 and \
            mCurProc.procInfo['state'] == 'READY' :
        return mCurProc

    if mQtFraction >= mUpperBound or \
            mCurProc.procInfo['finTime'] != -1 or \
            mCurProc.procInfo['state'] != 'READY' :

        if mQtFraction >= mUpperBound :
            mCurProc.procInfo['level'] += 1
        mQtFraction = 0

        mCurProc = None
        for p in procs :
            if not mCurProc :
                mCurProc = p
                continue
            a = p.procInfo['level']
            b = mCurProc.procInfo['level']
            if a < b :
                mCurProc = p

        mUpperBound = mCurProc.procInfo['level'] * qt
        
    mQtFraction += Clock.INTERVAL
    return mCurProc

