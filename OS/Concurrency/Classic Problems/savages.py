# Dining Savages Problem
# TODO : One of the savages may suffer from starvation
# Author : arashTaherK@gmail.com
from threading import Thread, Lock, Semaphore, Event
from random import random

lock = Lock()
potFull = Semaphore(0)
potEmpty = Semaphore(0)

MAX_CAPACITY = 3
MAX_COOK = 3    # How many times to refill the pot
NO_OF_SAVAGES = 3
potCap = MAX_CAPACITY     # Max pot capacity
cookIsDone = False

class Cook( Thread ):
    maxRefill = MAX_COOK

    def __init__( self ):
        Thread.__init__(self)

    def run( self ):
        global cookIsDone
        while Cook.maxRefill > 0 :
            # Wait till pot becomes empty
            potEmpty.acquire()
            self.serve()
            # Signal food is ready and pot is full
            potFull.release()
            Cook.maxRefill -= 1

        cookIsDone = True

    def serve( self ):
        print 'Cook is cooking'
        Event().wait( random() * 0.6 )
        print 'Cook finished cooking'


class Savage( Thread ):
    savageNo = 0

    def __init__( self ):
        Thread.__init__(self)
        Savage.savageNo += 1
        self.setName( 'Savage #' + `Savage.savageNo` )

    def run( self ):
        global potCap
        while not cookIsDone :
            lock.acquire()
            if ( potCap == 0 ) :
                if not cookIsDone :
                    potEmpty.release()
                    potFull.acquire()
                    # Cook has filled the pot, so :
                    potCap = MAX_CAPACITY
                else :
                    # If cook is finished and nothing left
                    lock.release()
                    break
            self.eat()
            potCap -= 1
            lock.release()

    def eat( self ):
        print self.getName() + ' is now eating'
        Event().wait( random() * 0.6 )
        print self.getName() + ' finished eating'

if __name__ == '__main__' :
    savages = [ Savage() for i in range(NO_OF_SAVAGES) ]
    cook = Cook()
    cook.start()

    for each in savages :
        each.start()

    cook.join()
    for each in savages :
        each.join()
