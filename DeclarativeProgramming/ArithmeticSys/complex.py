from table import put, get
import basePackage
import cmath

def Complex(a, b, form='rect'):
    if form=='rect':
        return Rect(real=a, img=b)
    elif form=='polar':
        return Polar(r=a, phi=b)
    else : raise Exception

class Rect:
    className = 'Rectangular'

    def __init__(self, real, img):
        self.real = real
        self.img = img

    def __str__(self):
        string = '(' + str(self.real)
        if self.img > 0:
            string += '+' + str(self.img) + 'i)'
        elif self.img < 0:
            string += '-' + str(self.img) + 'i)'
        return string

def installPackage():
    put('add', 'Rectangular Rectangular', add)

def add(c1, c2):
    return Complex( basePackage.add(c1.real, c2.real),
            basePackage.add(c1.img, c2.img), 'rect')

class Polar:
    className = 'Polar'

    def __init__(self, r, phi):
        self.r = r
        self.phi = phi
        self.rect = cmath.rect(r, phi)
