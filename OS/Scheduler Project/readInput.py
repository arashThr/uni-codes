from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from process import Process
from algorithm import Algorithm

class InputHandler(ContentHandler):
    totalMem = 0
    def __init__(self, processes, algorithms):
        ContentHandler.__init__(self)
        self.tag = ''
        self.attrs = []  # Used as temp var to hold attributes
        # Processes will be returned as a list of dicts
        self.proc = processes
        self.algs = algorithms
        self.totalMem = 0

    def startElement(self, name, attrs):
        if name == 'scheduler' :
            InputHandler.totalMem = attrs.values()[0]
        elif name == 'algorithm' :
            self.tag = 'algorithm'
            self.attrs.append( attrs.values() )
        elif name == 'process' :
            self.tag = 'process'
            # Start time and Mem usage of the proc are in attrs
            #print 'Process attrs are :', attrs.values()
            # Create a new process and add it into our process list
            self.proc.append( Process( attrs.values() ) )
        elif name == 'io' :
            self.tag = 'io'
            self.proc[-1].AddIOInfo( attrs.values() )
        elif name == 'cpu' :
            self.tag = 'cpu'

    def endElement(self, name):
        if name=='algorithm' :
            self.tag = ''
            self.attrs = []
        elif name == 'io' or name == 'cpu' or name == 'processes' :
            self.tag = ''
            
    def characters(self, string):
        if self.tag == 'algorithm' :
            # Insert name of the alg at first
            self.algs.activateAlg( string.strip(), self.attrs )
            #print string
            #print self.attrs
        elif self.tag == 'cpu' :
            #print 'CPU is :', string
            self.proc[-1].addBurst( string.strip() )
        elif self.tag == 'io' :
            #print 'IO is :', string
            self.proc[-1].addBurst( string.strip() )

def readInput(inputAddr='input.xml') :
    alg = Algorithm()
    allProc = []
    parser = make_parser()
    parser.setContentHandler( InputHandler(allProc, alg ) )
    parser.parse(inputAddr)
    return (InputHandler.totalMem, allProc, alg )

if __name__ == '__main__' :
    readInput()
