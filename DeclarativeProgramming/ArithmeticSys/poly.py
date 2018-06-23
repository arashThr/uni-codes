from table import put, get
import basePackage

class Poly:
    '''Polynomial numbers : A list of coefficient, power pairs'''
    # -We can retrieve calss name by obj.__class__.__name__
    # But using class variables in cleaner
    # -Using a ilst of dictionaris can improve readability
    # Poly[i][0] -> Coeff, Poly[i][1] -> Power
    className = 'Poly'
    def __init__(self, param, *args):
        if len(param)!=1 or not isinstance(param, str):raise Exception
        self.param = param
        self.poly = []
        # Sort list in descending order
        self.poly = sorted(args, compare, None, True)
        #[self.poly.append(term) for term in args]

    def __str__(self):
        output = ''
        for term in self.poly:
            output += str(term[0]) + self.param + '^' + str(term[1]) + ' + '
        return output[0:-3]

    def __len__(self):
        l = 0
        for item in self.poly:
            l += 1
        return l

    def __getitem__(self, key):
        return self.poly[key]

# Used in sorted to sort polynomials based on their power
def compare(a, b):
    if a[1] < b[1]:
        return -1
    elif a[1] == b[1]:
        return 0
    return 1

def installPackage():
    put('add', 'Poly Poly', add)
    put('mul', 'Poly Poly', mul)

# Another approach to add and multiply
def simplifyPoly(poly):
    pass

def add(poly1, poly2):
    if poly1.param != poly2.param : raise Exception
    newPoly = []
    i = j = 0

    while i<len(poly1) and j<len(poly2):
        if poly1[i][1] == poly2[j][1]: # Powers are equal
            # We use add to add two parts
            s = basePackage.add(poly1[i][0], poly2[j][0])
            p = poly1[i][1]
            newPoly.append((s, p))
            i += 1
            j += 1
        elif poly1[i][1] > poly2[j][1]:
            newPoly.append((poly1[i][0], poly1[i][1]))
            i += 1
        else:
            newPoly.append((poly2[j][0], poly2[j][1]))
            j += 1

    while i<len(poly1):
        newPoly.append((poly1[i][0], poly1[i][1]))
        i += 1
    while j<len(poly2):
        newPoly.append((poly2[j][0], poly2[j][1]))
        j += 1

    return Poly(poly1.param, *newPoly)

# TODOx : Return value is not sorted
# Solved -> I needed to define comparisions in ordinary
def mul(poly1, poly2):
    if poly1.param != poly2.param : raise Exception
    newPoly = []
    i = j = 0

    while i<len(poly1):
        while j<len(poly2):
            coeff = basePackage.mul(poly1[i][0], poly2[j][0])
            power = basePackage.add(poly1[i][1], poly2[j][1])
            newPoly.append( (coeff, power) )
            j += 1
        j = 0
        i += 1

    return Poly(poly1.param, *newPoly)


def sub() : raise NotImplemented
def div() : raise NotImplemented
