# Hackers-Employees-Crossing-River problem
# Either one type or same number of each one
# can be settled in a boat
# Only one boat crossing river at a time
from threading import Lock, Condition, Thread, Event, Semaphore
from random import shuffle, random
from sys import exit


totalHackers = 2
totalEmployees = 2
boatCapacity = 2

# How many hacker and employee have anounced 
# thier request to get in boat
noOfHackers = 0
noOfEmployees = 0
# Number of current passengers in boat
boatPassengers = 0

# Used to protect access to number of
# hackers and employees
mutex = Lock()

hackersQueue = Semaphore(0)
employeesQueue =  Semaphore(0)

# Takes care of access to boatPassenger
boatLock = Lock()
boatFull = Condition( boatLock )

#hackersLock = Lock()
#empsLock = Lock()
#hackersQueue = Condition( hackersLock )
#employeesQueue = Condition( empsLock )

class Hacker( Thread ):
    hackerNo = 0

    def __init__( self ):
        Thread.__init__(self)
        #self.setDaemon(True)
        self.isCaptain = False
        Hacker.hackerNo += 1
        self.setName('Hacker #' + `Hacker.hackerNo`)

    def run( self ):
        global noOfHackers
        global noOfEmployees
        global boatPassengers
        halfBoatSize = boatCapacity/2

        mutex.acquire()
        noOfHackers += 1
        if noOfHackers == boatCapacity :
            noOfHackers = 0
            for i in range(boatCapacity) :
                #hackersQueue.notify(3)
                hackersQueue.release()
            self.isCaptain = True
        elif noOfHackers == halfBoatSize and \
                noOfEmployees >= halfBoatSize :
                    noOfHackers = 0
                    noOfEmployees -= halfBoatSize
                    for i in range (halfBoatSize) :
                        hackersQueue.release()
                        employeesQueue.release()
                    self.isCaptain = True
        else :
            mutex.release()
        
        # Using conditions is harder than creating a queue
        # by semaphores
        # We cann't use captain to notifyAll
        # How do we know avery one arrived ?
        #if not self.isCaptain :
            #hackersQueue.acquire()
        hackersQueue.acquire()
        # Other option is to send siganl after each wait

        boatLock.acquire()
        board(self)
        boatPassengers += 1
        if boatPassengers != boatCapacity :
            print self.getName() + ' waits for other passengers'
            boatFull.wait()
        else :
            print self.getName() + ' arrival made boat full'
            boatPassengers = 0
            boatFull.notifyAll()
        boatFull.release()

        if self.isCaptain :
            rowBoat( self )
            mutex.release()


class Employee( Thread ):
    empNo = 0

    def __init__( self ):
        Thread.__init__(self)
        #self.setDaemon(True)
        self.isCaptain = False
        Employee.empNo += 1
        self.setName('Employee #' + `Employee.empNo`)

    def run( self ):
        global noOfEmployees
        global noOfHackers
        global boatPassengers
        halfBoatSize = boatCapacity/2

        mutex.acquire()
        noOfEmployees += 1
        if noOfEmployees == boatCapacity :
            noOfEmployees = 0
            for i in range(boatCapacity) :
                employeesQueue.release()
            self.isCaptain = True
        elif noOfEmployees == halfBoatSize and \
                noOfHackers >= halfBoatSize :
                    noOfEmployees = 0
                    noOfHackers -= halfBoatSize
                    for i in range (halfBoatSize) :
                        hackersQueue.release()
                        employeesQueue.release()
                    self.isCaptain = True
        else :
            mutex.release()
        
        employeesQueue.acquire()

        boatLock.acquire()
        board(self)
        boatPassengers += 1
        if boatPassengers != boatCapacity :
            print self.getName() + ' waits for other passengers'
            boatFull.wait()
        else :
            print self.getName() + ' arrival made boat full'
            boatPassengers = 0
            boatFull.notifyAll()
        boatFull.release()

        if self.isCaptain :
            rowBoat( self )
            mutex.release()


def board( passenger ):
    print passenger.getName() + ' setteled in boat'

def rowBoat( captain ):
    Event().wait(random()*.6)
    print captain.getName() + ' boat reached to the other side'


if __name__ == '__main__' :
    if totalHackers%boatCapacity != 0 and \
        totalHackers%boatCapacity != boatCapacity :
            print 'Incorrect input'
            exit()
    hackers   = [ Hacker() for i in range (totalHackers) ]
    employees = [ Employee() for i in range (totalEmployees) ]
    
    travelers = hackers + employees
    shuffle( travelers )
    
    for person in travelers :
        person.start()
    for person in travelers :
        person.join()

