# Dining philosophers problem
# Tanenbaum solution
from threading import Thread, Semaphore, Lock, Event
from random import shuffle, random, randint

# How many philosophers ar at the table
noOfPhils = 3
# How many meals they want to serve will be
# a random number between 1 and rounds
rounds = 2

state = ['thinking'] * noOfPhils
# Determines whether a philospher can start eating or not
sem = [ Semaphore(0) for i in range(noOfPhils) ]
# To lock the table so we can decide
mutex = Lock()

class DP( Thread ):
    '''Dininig philosopher class'''
    pid = 0

    def __init__( self ):
        Thread.__init__(self)
        self.setName( 'Philosopher #' + `DP.pid` )
        self.pid = DP.pid
        DP.pid += 1

    def run( self ):
        isAtTable = randint( 1, rounds )
        while isAtTable :
            self.think()
            self.getFork()
            self.eat()
            self.putFork()
            isAtTable -= 1

    def getFork( self ):
        mutex.acquire()
        print self.getName() + ' getting fork'
        state[self.pid] = 'hungary'
        self.test( self.pid )
        mutex.release()
        sem[ self.pid ].acquire()

    def putFork( self ):
        mutex.acquire()
        print self.getName() + ' puting fork'
        state[self.pid] = 'thinking'
        self.test( left( self.pid ) )
        self.test( right( self.pid ) )
        mutex.release()

    def test( self, i ):
        if state[ left( i ) ] != 'eating' and \
        state[ right( i ) ] != 'eating' and \
        state[ i ] == 'hungary' :
            state[ i ] = 'eating'
            sem[ i ].release()

    def think( self ):
        #print self.getName() + ' is thinking'
        Event().wait(random()*.6)
        #print self.getName() + ' fininshed thinking'

    def eat( self ):
        print self.getName() + ' is eating'
        Event().wait(random()*.6)
        #print self.getName() + ' finished eating'

def right( i ) : return (i+1) % noOfPhils
def left( i ) : return (i+noOfPhils-1) % noOfPhils


if __name__ == '__main__' :
    phils = [ DP() for i in range(noOfPhils) ]
    shuffle( phils )

    for each in phils :
        each.start()
    for each in phils :
        each.join()
