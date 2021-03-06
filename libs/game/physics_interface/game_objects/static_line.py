from editable import Editable
from _env import *

class UserStaticLine( Editable ):
    color    = (0,1,0,1)
    colltype = COLLTYPE_USERPLAT

    def adjust_coordinates( self, (ox, oy), (xdim, ydim) ):
        # Find absolute postion based on the passed-in pos and size.
        self.points = self.get_start(), self.get_end()
