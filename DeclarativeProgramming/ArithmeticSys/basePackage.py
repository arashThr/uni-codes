# Definitions of genral functions
from ordinary import Ordinary
from table import get, put

# Data preperation for operation
# Int will be change into ordinary
# Casting will done, if required
def prepareOperands(a, b=None):
    '''Operands are input
    Modified operands and their type is output'''
    if isinstance(a, int):
        opType = 'Ordinary'
        a = Ordinary(a)
        if isinstance(b, int):
            opType += ' Ordinary'
            b = Ordinary(b)
    else:
        opType = a.className
        if b:
            opType += ' ' + b.className
    return (a, b, opType)


def add(a, b):
    a, b, opType = prepareOperands(a, b)
    return get('add', opType)(a, b)

def sub(a, b):
    a, b, opType = prepareOperands(a, b)
    return get('sub', opType)(a, b)

def mul(a, b):
    a, b, opType = prepareOperands(a, b)
    return get('mul', opType)(a, b)

def div(a, b):
    a, b, opType = prepareOperands(a, b)
    return get('div', opType)(a, b)

def neg(a):
    a, _, opType = prepareOperands(a)
    return get('neg', opType)(a)

def rev(a):
    a, _, opType = prepareOperands(a)
    return get('rev', opType)(a)


class BaseOperation:
    className = ''
    definedOps = ['add', 'sub', 'mul', 'div']

    @staticmethod
    def installPackage():
        raise NotImplemented
    def __str__(self):
        raise NotImplemented
    def add(self, other):
        raise NotImplemented
    def sub(self, other):
        raise NotImplemented
    def mul(self, other):
        raise NotImplemented
    def div(self, other):
        raise NotImplemented
