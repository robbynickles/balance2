from cymunk import Vec2d

from utils import distance
from libs.game.physics_interface.game_objects.level_build.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT, COLLTYPE_LAVA, COLLTYPE_USERCURVE

def connect( self, pos ):
    """Search for any user-drawn platforms near pos. If one is found see if pos is
    close to either of its endpoints. If it is near an endpoint, set pos to that endpoint."""
    MAX_DIST = 30
    shape    = self.physics_interface.space.nearest_point_query_nearest( Vec2d( *pos ), 
                                                                         MAX_DIST, 
                                                                         COLLTYPE_USERPLAT | COLLTYPE_LAVA | COLLTYPE_USERCURVE )

    if shape:

        # Make sure magnets only connect two endpoints from different lines.
        touching_line = self.physics_interface.smap[ shape ]
        if touching_line != self.target_line and \
           ( shape.collision_type == COLLTYPE_USERPLAT or shape.collision_type == COLLTYPE_LAVA or shape.collision_type == COLLTYPE_USERCURVE ):

            if shape.collision_type == COLLTYPE_LAVA:
                start = touching_line.points[:2]
                end   = touching_line.points[2:]
            else:
                start = touching_line.get_start()
                end   = touching_line.get_end() 

            if distance( start, pos ) <= MAX_DIST:
                pos = Vec2d( *start )
            elif distance( end, pos ) <= MAX_DIST:
                pos = Vec2d( *end )

    return pos
