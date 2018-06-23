from Queue import Queue
from time import sleep
import sys
import os

from process import Process
from algorithm import Algorithm
from readInput import readInput
from io import IOHandler
from clock import Clock

class Scheduler :
    # The system has not been started
    #curTime = -1
    clk = Clock()
    procSelected = False

    waitingQ = []
    readyQ = []
    swapedOut = []

    def __init__(self, inputFile) :
        # Read input
        self.totalMem, self.procs, self.alg = readInput(inputFile)
        self.totalMem = int( self.totalMem )
        self.usedMem = 0
        self.totalNoOfProcs = len( self.procs )
        # Create and start IO handler
        handleIO = IOHandler()
        handleIO.start()

        #self.alg.showAlgs()

        #print '\nProcesses are :'
        #for p in self.procs :
            #p.showProcInfo()


    def startScheduling( self ):
        print 'System starts up'
        # Last process to run
        # We use it to show CPU users change
        prevProc = None
        # Loop until a algorithm selected
        #while not
            #Scheduler.curTime += 1
            #sleep(INTERVAL)

        while self.totalNoOfProcs > 0 :
            # Tick Tock
            Scheduler.clk.incTime()
            self.curTime = Scheduler.clk.getTime()
            self.repTime = Scheduler.clk.repTime()

            #print 'CurTime :', Scheduler.repTime

            # Check to see if new process attended to system
            for p in self.procs :
                #print 'Start :', p.procInfo['start']  
                if p.procInfo['start'] <= self.curTime and \
                        not p.procInfo['hasStarted'] :
                    if p.procInfo['mem']+self.usedMem > self.totalMem :
                        print self.repTime, p.showPID(), '-> swaped out'
                        self.swapedOut.append( p )
                        p.procInfo['hasStarted'] = True
                    else :
                        self.addNewProc( p )

            #print 'Len :', len( self.swapedOut )
            #print 'Total :', self.totalMem
            #print 'Used :', self.usedMem
            for p in self.swapedOut :
                if p.procInfo['mem'] <= self.totalMem-self.usedMem :
                    self.addNewProc( p )
                    self.swapedOut.remove( p )
                    print self.repTime, p.showPID(), '-> swaped in'
                    
            # Select an algorithm based on current time
            self.alg.selectAlg( Scheduler.clk )

            # If no algorithm is selected OR
            # All processes are in wating queue ...
            if not Algorithm.algSelected :
                sleep(Clock.INTERVAL)   # wait for a sec and
                continue    # continue
            #print 'Alg is :', self.alg.curAlgName

            # If no proc is in eady list, it means they're waiting
            # Let's check to see if they have been completed
            if len( Scheduler.readyQ ) == 0 :
                self.checkIO()
                sleep(Clock.INTERVAL)   # wait for a sec and
                continue

            # Select next process to run based on algorithm
            # If algorithm is preemptive, in each interval check ready queue
            # If it's nonpreemptive, check it when previous process finished CPU
            if Algorithm.isPreemptive or not Scheduler.procSelected :
                nxtProc = self.alg.chooseProc( Scheduler.readyQ, Scheduler.clk )
                Scheduler.procSelected = True
            if nxtProc == None :
                sleep(Clock.INTERVAL)
                continue
            
            if nxtProc != prevProc :
                if prevProc != None :
                    print self.repTime, prevProc.showPID(), '-> Finished CPU'
                prevProc = nxtProc
                print self.repTime, nxtProc.showPID(), '-> CPU'

            #print 'Nxt proc :', nxtProc.procInfo['pid']

            # Run next process
            nxtProc.runProc(Clock.INTERVAL)
            # Give it time to run ...
            sleep(Clock.INTERVAL)
            # And now check its start

            # Check executed process state
            self.checkState(nxtProc)

            # Chech IO devices
            self.checkIO()

        # Send signal to IO to terminate
        IOHandler.IOReqQ.put( None )
        
        print 'System is shutting down, Bye'


    def giveTicket( self, proc, noOfTickets=10 ):
        if len( Algorithm.tickets ) < noOfTickets :
            raise RuntimeError, 'Insufficient funds'
        for i in range( noOfTickets ):
            ticket = Algorithm.tickets.pop(0) 
            proc.tickets.append( ticket )
            Algorithm.assignedTickets.append( ticket )

    def retrieveTicket( self, proc ):
        for i in range( len( proc.tickets ) ) :
            ticket = proc.tickets.pop()
            Algorithm.tickets.append( ticket )
            Algorithm.assignedTickets.remove( ticket )

    def showStatus( self, proc ):
        TAT = proc.procInfo['finTime'] - proc.procInfo['start']
        if TAT - proc.totalBursts < 0.1:
            waiting = 0
            util = 1
        else :
            waiting = int(TAT) - int(proc.totalBursts)
            util = waiting / TAT
        print ': W:', waiting, ',T:', TAT, ',U:', str(int(util*100))+'%'


    # Add process P to ready queue and other queues ( for algs )
    def addNewProc( self, p ):
        print self.repTime, p.showPID(), 'Created'
        p.procInfo['hasStarted'] = True
        # Add newly create process to ready list
        print self.repTime, p.showPID(), '-> readyQ'

        Scheduler.readyQ.append( p )
        #Algorithm.RRQ.put( p )
        self.giveTicket( p )

        self.usedMem += p.procInfo['mem']

    # Check state after CPU burst has been done
    def checkState( self, proc ):
        state = proc.procInfo[ 'state' ]
        if state == 'FINISHED' :
            print self.repTime, proc.showPID(), 'Finished',
            proc.procInfo['finTime'] = self.curTime
            self.showStatus(proc)

            # WE WILL PUT OTHER DATA ABOUT PROC IN HERE
            #self.procs.remove( proc )
            Scheduler.readyQ.remove( proc )

            self.totalNoOfProcs -= 1
            Scheduler.procSelected = False
            # Give back it's tickets
            self.retrieveTicket( proc )
            self.usedMem -= proc.procInfo['mem']
        elif state == 'WAITING' :
            print self.repTime, proc.showPID(), '-> WaitingQ'
            Scheduler.waitingQ.append( proc )
            # Remove it from ready list

            #print 'Len readQ :', len( Scheduler.readyQ )
            #print 'Cur proc :', proc.procInfo['pid'], proc.tickets
            #print 'Proces :', Scheduler.readyQ[0].procInfo['pid'], proc.tickets
            Scheduler.readyQ.remove( proc )
            Scheduler.procSelected = False
            # We have to start a thread to run this process
            # when io finished we should put proc in ready Q again
            self.retrieveTicket( proc )
            # Put proc in IO queue
            IOHandler.IOReqQ.put( proc, True )
            
        elif state == 'READY' :
            # Process used up it's quantum
            # TODO : We have to give back one of it's tickets
            pass
        else :
            raise RuntimeError, 'Error occured, unkown state'

    # Check after IO burst has been done
    def checkIO( self ):
        # In here we should check to see if any IO has been finished
        # Add proc to ready Q again
        while not IOHandler.IOFinQ.empty() :
            p = IOHandler.IOFinQ.get()
            #print 'IO finished for :', p.procInfo['pid']

            # Updating process statics
            p.bursts.pop(0)
            p.IOInfo.pop(0)
            p.procInfo['state'] = 'READY'
            p.procInfo['noOfEvents'] -= 1
            p.curBurst = 'CPU'
            # Add it to ready list
            if p.procInfo['noOfEvents'] == 0 :
                print self.repTime, p.showPID(), 'Finished',
                p.procInfo['finTime'] = self.curTime
                self.showStatus( p )
                self.totalNoOfProcs -= 1
                self.usedMem -= p.procInfo['mem']
            else :
                print self.repTime, p.showPID(), '-> readyQ again'
                Scheduler.readyQ.append( p )
                # Reset process level in MLFQ algorithm
                p.procInfo['level'] = 1
                # Give it back some tickets
                self.giveTicket( p )


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: %s XML-File' % sys.argv[0])

    if not os.path.exists(sys.argv[1]):
        sys.exit('ERROR: XML file %s was not found!' % sys.argv[1])
    sch = Scheduler(sys.argv[1])
    print '\nNOW ...'
    sch.startScheduling()
