from table import put, get

class Ordinary:
    className = 'Ordinary'
    def __init__(self, n):
        self.num = n
    def __str__(self):
        return str(self.num)
    # Take a look at __str__ in Rect to see why we need these
    def __gt__(self, op):
        return self.num > op
    def __lt__(self, op):
        return self.num < op
    def __eq__(self, op):
        return self.num==op

def installPackage():
    put('neg', 'Ordinary', neg)
    opType = 'Ordinary Ordinary'
    opList = [('add', add), ('sub', sub), ('mul', mul), ('div', div)]
    [put(op[0], opType, op[1]) for op in opList]

def add(op1, op2):
    return Ordinary(op1.num + op2.num)

def sub(op1, op2):
    return Ordinary(op1.num - op2.num)

def mul(op1, op2):
    return Ordinary(op1.num * op2.num)

def div(op1, op2):
    return Ordinary(op1.num / op2.num)

def neg(op):
    return Ordinary(-op1.num)
