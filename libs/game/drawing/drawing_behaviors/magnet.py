from cymunk import Vec2d

from utils import distance
from libs.game.physics_interface.game_objects.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT

def connect( self, pos ):
    """Search for any user-drawn platforms near pos. If one is found see if pos is
    close to either of its endpoints. If it is near an endpoint, set pos to that endpoint."""
    MAX_DIST = 40
    shape    = self.physics_interface.space.nearest_point_query_nearest( Vec2d( *pos ), 
                                                                         MAX_DIST, 
                                                                         COLLTYPE_USERPLAT )
    if shape and shape.collision_type == COLLTYPE_USERPLAT:
        userline = self.physics_interface.smap[ shape ]
        start    = userline.points[:2]
        end      = userline.points[2:]

        if distance( start, pos ) <= MAX_DIST:
            pos = Vec2d( *start )
        elif distance( end, pos ) <= MAX_DIST:
            pos = Vec2d( *end )

    return pos
