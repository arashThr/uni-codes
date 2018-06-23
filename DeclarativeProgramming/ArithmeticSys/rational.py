from table import put, get

class Rational:
    className = 'Rational'
    def __init__(self, n, d):
        if d < 0:
            n = -n
            d = -d
        self.gcd = abs(gcd(max(n,d), min(n,d)))
        self.numer = n/self.gcd
        self.denom = d/self.gcd
    def __str__(self):
        string = 'Rational : ' + str(self.numer)
        if self.denom != 1 : string += '/' + str(self.denom)
        return string

def gcd(a, b):
    if b==0:
        return a
    else:
        return gcd(b, a%b)

def installPackage():
    opType = 'Rational Rational'
    opList = [('add', add), ('sub', sub), ('mul', mul), ('div', div)]
    [put(op[0], opType, op[1]) for op in opList]

    put('neg', 'Rational', neg)
    put('rev', 'Rational', rev)

def add(op1, op2):
    return Rational(op1.numer*op2.denom+op2.numer*op1.denom, 
            op1.denom*op2.denom)

def sub(op1, op2):
    return add(op1, neg(op2))

def mul(op1, op2):
    return Rational(op1.numer*op2.numer, op1.denom*op1.denom)

def div(op1, op2):
    return mul(op1, rev(op2))

def neg(op):
    return Rational(-op.numer, op.denom)

def rev(op):
    return Rational(op.denom, op.numer)
