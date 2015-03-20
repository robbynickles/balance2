from _env import *
from editable import Editable
from static_curve_utils import fit_curve

class UserStaticCurve( Editable ):
    color    = (1,0,1,1)
    colltype = COLLTYPE_USERCURVE
    curve    = True

    def adjust_coordinates( self, (ox,oy), (xdim,ydim) ):
        # Find absolute postion based on the passed-in pos and size.
        a, b, c     = self.get_start(), self.get_thirdpt(), self.get_end()

        # Generate a segementation that approximates the curve.
        self.points = fit_curve( [ a, b, c ] )
