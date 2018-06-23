# Sleeping barber shop using semaphores
# TODO : Jobs to do in getHairCut and cutHair are a litte vague
# Author : arashTaherK@gmail.com
from threading import Thread, Semaphore, Lock, Event
from random import random

lock = Lock()
costumerReady = Semaphore(0)
barberReady = Semaphore(0)

MAX_COSTUMERS = 7
seats = 1   # Number of available seats, except barber chair
shopIsOpen = True
totalCusts = 0

class Customer( Thread ):
    noOfCusts = 0
    custId = 1

    def __init__( self ):
        Thread.__init__( self )
        self.setName( 'Customer #' + `Customer.custId` )
        Customer.custId += 1

    def run( self ):
        global seats, shopIsOpen, totalCusts
        lock.acquire()
        print self.getName() + ' arrived'
        # Seats plus one sitting on barber chair
        if Customer.noOfCusts == seats + 1 :
            print self.getName() + ' is leaving'
            lock.release()
            totalCusts += 1
            return
        Customer.noOfCusts += 1
        lock.release()

        # Rendezvous
        costumerReady.release()
        barberReady.acquire()
        self.getHairCut()

        # Decrease number of customers
        lock.acquire()
        Customer.noOfCusts -= 1
        lock.release()

    def getHairCut( self ):
        print self.getName() + ' is getting hair cut'
        #Event().wait( randome() % .6 )
        print self.getName() + ' is done'



class Barber( Thread ):
    def __init__( self ):
        Thread.__init__(self)

    def run( self ):
        global shopIsOpen, totalCusts
        while shopIsOpen :
            # If no there's customer sleep, otherwise
            # Let one costumer to sit on the chair
            # Rendezvous
            costumerReady.acquire()
            barberReady.release()

            self.cutHair()

            # TODO : IN HERE WE MAY NEED A LOCK
            totalCusts += 1

            # If this is the last customer, close the shop
            if totalCusts == MAX_COSTUMERS :
                print 'Close shop'
                shopIsOpen = False

    def cutHair( self ):
        print 'Baber started cutting hair'
        Event().wait( random() % .6 )

if __name__ == '__main__' :
    costs = [ Customer() for i in range( MAX_COSTUMERS ) ]
    barber = Barber()

    barber.start()
    for each in costs :
        Event().wait( random() % .8 )
        each.start()

    barber.join()
    for each in costs :
        each.join()

