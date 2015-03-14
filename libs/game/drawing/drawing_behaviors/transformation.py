##### Acceleromter ---> Tilt mapping helpers.
def normalize( x ):
    "Normalize x (get the direction of the vector)."
    return abs(x) / x
    
def combine( a, b ):
    "Combine a and b to form a Pythagorean diagonal."
    return ( a**2 + b**2 ) ** .5
        
def transfer_acceleration( z ):
    "Return a function that adds z-axis acceleration to an axis."
    A = 1 - z**2
    def add_z( acc ):
        return normalize( acc ) * combine( acc, (acc**2/A)*abs(z) )
    return add_z

def to_tilt( (x,y,z) ):
    try:
        add_z = transfer_acceleration( z )
        return add_z( x ), add_z( y )
    except:
        # Probably a ZeroDivision error because either the device-motion updates haven't started,
        # or the phone is flat (z^2 = 1 ====> A = 0 ====> x^2/A ====> undefined )
        return 0, 0

def horizontal_line( tilt, ox ):
    """ (line perpendicular to the current gravity)
    Return a function that represents the equation of a line 
    with a slope of tilt[1] / tilt[0] 
    centered at (ox, 0) """
    run, rise = tilt
    if run != 0:
        return lambda x: rise/run * x + ox
    else:
        return lambda x: 0


