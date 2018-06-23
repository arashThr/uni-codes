#!/usr/bin/python
# arashTaherK@gmail.com
from time import time
from sys import exit
from threading import Thread
from multiprocessing import cpu_count

# Initilialization of variables
f = open( 'puzzle.txt' )
puzzle = [ [ int(a) for a in line.split() ] for line in f.readlines() ]
# Extract block size
BS = int( puzzle.pop(0)[0] )
SIZE = BS * BS
numsRange = range( 1, SIZE+1 )
CORES_NUM = cpu_count()

def row( i, grid ):
    '''Return i-th row of grid'''
    return grid[i]

def col( j, grid ):
    '''Retun j-th column of grid'''
    return [ grid[i][j] for i in range(SIZE) ]

def block( i, j, grid ):
    '''Retun a list of elements in i,j block'''
    return [ grid[ (i/BS)*BS+a ][ (j/BS)*BS+b] \
            for a in range(BS) for b in range( BS ) ]

def missing( lst ):
    '''Retun missing elements in the list'''
    return [ x for x in numsRange if x not in lst ]

def possible(i, j):
    '''Return possible elements for a single cell'''
    if puzzle[i][j] : return [] # This element already has a value
    else :
        return [ x for x in numsRange if x in missing( row(i, puzzle) ) and \
                x in missing( col(j, puzzle) ) and x in missing( block(i, j, puzzle ) ) ]

def makePossibles( pos, start=0, end=SIZE ):
    '''Create a mtrix of possibilities for puzzle'''
    for i in range(start, end):
        for j in range(SIZE):
            pos[i][j] = possible( i, j )

def drop( lst, i ):
    '''Drop i-th element from the list'''
    return [ lst[j] for j in range( len(lst) ) if i != j ]

def flatten( lst ):
    '''Tranform a list of list onto a single list'''
    return [ x for y in lst for x in y ]

def checkAllBut( x, lst, pos ):
    '''Check existence of x in list, except `pos' position
    Returns True if x doesn't exist in flatten list'''
    return x not in flatten( drop( lst, pos ) )


def checkSolution() :
    '''Check to see if answer is correct'''
    for i in range(SIZE) :
        for j in range(SIZE) :
            if puzzle[i][j] == 0 :
                print 'Cell %d, %d has conflict' % (i+1, j+1)
                return False
                #continue
            if puzzle[i][j] in drop ( block(i, j, puzzle), \
                    (i%BS)*BS + j%BS ) or \
                    puzzle[i][j] in drop( row(i, puzzle), j ) or \
                    puzzle[i][j] in drop( col(j, puzzle), i ) :
                        print 'Cell %d, %d has conflict' % (i, j)
                        return False
            #if puzzle[i][j] in drop ( block(i, j, puzzle), (i%3)*3 + j%3 ) :
                #print 'qqqCell %d, %d has conflict' % (i+1, j+1)
                #return False

            #if puzzle[i][j] in drop( row(i, puzzle), j ) :
                #print 'aaaCell %d, %d has conflict' % (i+1, j+1)
                #return False
            #if puzzle[i][j] in drop( col(j, puzzle), i ) :
                #print 'zzzCell %d, %d has conflict' % (i+1, j+1)
                #return False
    return True


def checkInput( puzzle ):
    for i in range(SIZE) :
        for j in range(SIZE) :
            elem = puzzle[i][j]
            if elem == 0 :
                continue
            elif ( elem in drop( row(i, puzzle), j ) or \
                    elem in drop( col(j, puzzle), i ) or
                    elem in drop ( block(i, j, puzzle), (i%BS)*BS + j%BS ) ) :
                print 'I :', i, 'J :', j, '->', elem
                print drop( row(i, puzzle), j )
                print drop( col(j, puzzle), i )
                print drop( block(i, j, puzzle), (i%BS)*BS + j%BS )
                return False
    return True



def threadSolvePuzzle():
    '''If a value appeard  only once in it row, col or block
    although there are multiple posiible value in it's set,
    we can choose that one'''
    changed = True
    while changed :
        changed = False
        # All possiblities for all cells
        possibles = [ [ 0 for i in range(SIZE) ] for j in range(SIZE) ]

        threads = []
        start = 0
        chunk = ( SIZE / CORES_NUM ) + 1

        for t in range( CORES_NUM ) :
            end = start+chunk
            if end > SIZE :
                end = SIZE
            threads.append( Thread( target=makePossibles, args=(possibles, start, end ) ) )
            threads[t].start()
            start += chunk

        # Wait for threads to terminate
        for t in range( CORES_NUM ):
            threads[t].join()

        for i in range(SIZE) :
            for j in range(SIZE) :
                # If only one value in the list, choose it
                if len( possibles[i][j] ) == 1 :
                    puzzle[i][j] = possibles[i][j][0]
                    changed = True
                # For all the possible values in current cell, check to see
                # if it is unique or not
                for x in possibles[i][j] :
                    if ( checkAllBut(x, block(i, j, possibles), \
                            (i%BS)*BS + j%BS ) or \
                            checkAllBut( x, col(j, possibles), i ) or \
                            checkAllBut( x, row(i, possibles), j ) ) :
                        changed = True
                        puzzle[i][j] = x

    print
    if checkSolution() :
        print 'A possible sulotion is :'
        printPuzzle(puzzle)
    else :
        print 'We couldn\' find any solution'
        printPuzzle(puzzle)


def printPuzzle( puzzle ):
    for i in range(SIZE):
        for j in range(SIZE):
            print puzzle[i][j], '\t',
        print



if __name__ == '__main__' :
    printPuzzle(puzzle)
    if checkInput( puzzle ) :
        print 'Input is OK'
    else :
        print 'Input is Not OK'
        exit()

    print
    start = time()
    threadSolvePuzzle()
    elapsed = time() - start
    print 'Elapsed time :', elapsed

