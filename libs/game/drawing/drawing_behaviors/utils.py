def distance( a, b ):
    return sum ( [ (x1-x2)**2 for x1,x2 in zip( a, b ) ] ) ** .5
        
