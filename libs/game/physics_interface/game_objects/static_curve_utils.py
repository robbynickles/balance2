from pycurve import Bspline

def distance( a, b ):
    return sum ( [ (x1-x2)**2 for x1,x2 in zip( a, b ) ] ) ** .5

def polylen( P ):
    assert len( P ) == 3
    a,b,c           = P
    return distance( a,b ) + distance( b, c )

def hyperbola( x ):
    return ( 1 + x*x ) ** .5

def fit_curve( P ):
    n  = len(P) - 1 
    k  = 2          
    m  = n + k + 1  
    _t = 1 / (m - k * 2) 
    
    # Generate a domain.
    t = k * [0] + [t_ * _t for t_ in xrange(m - (2 * k) + 1)] + [1] * k
    
    # Generate a range over the domain that includes the y-values in P.
    S = Bspline(P, t, k)
    
    points  = []

    # The number of segments approximating S is proportional to the length of the polyline formed by P.
    SEGS    = .03 * hyperbola( polylen( P ) )
    for i in xrange( int(SEGS) ):
        try:
            points += [ S( i / SEGS ) ]
        except AssertionError:
            continue # argument not in domain.

    return points + [P[-1]] # Manually include the end in the segmentation.
