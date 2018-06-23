from rational import Rational
from ordinary import Ordinary
from poly import Poly
from complex import Complex
import rational
import ordinary
import poly
import complex
from table import get, put
from basePackage import add, sub, mul, div, neg, rev

if __name__=='__main__':
    # At first, let's install numbers packages
    rational.installPackage()
    ordinary.installPackage()
    poly.installPackage()
    complex.installPackage()
    
    r1 = Rational(1,5)
    r2 = Rational(2,5)
    o1 = Ordinary(3)
    o2 = Ordinary(8)

    r3 = rational.add(r1, r2)
    print r3
    o3 = ordinary.add(o1, o2)
    print o3

    print 'Neg :', neg(r1)
    print 'Rev :', rev(r1)
    
    print 'Ord :', add(3, 4)

    p1 = Poly( 'x', (1,1), (3,3), (2,2) )
    print 'Poly :', p1
    p2 = Poly( 'x', (1,1), (3,3), (2,2) )
    print 'ADD :', add(p1, p2)
    print 'MUL :', mul(p1, p2)

    # Complex numbers
    c1 = Complex(1, 2, 'rect')
    print 'C1 :', c1
    c2 = Complex(2, 3, 'rect')
    print 'C2 :', c2
    print 'C1 + C2 :', add(c1, c2)
