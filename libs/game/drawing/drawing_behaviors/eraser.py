from kivy.graphics import Color, Line
from cymunk import Vec2d

import cymunk as cy

from libs.game.physics_interface.game_objects.collision_handlers import COLLTYPE_DEFAULT, COLLTYPE_BALL, COLLTYPE_USERPLAT

def erase( self, touch, touch_stage ):
    """Do three different things depending on which touch_stage it is."""
    MAX_DIST = 25
    if touch_stage == 'touch_down':
        # Check if there are any shapes within MAX_DIST. Remove them.
        shape = self.physics_interface.space.nearest_point_query_nearest( Vec2d( *touch.pos ), MAX_DIST, COLLTYPE_USERPLAT )
        if shape and shape.collision_type == COLLTYPE_USERPLAT:
            self.physics_interface.smap[ shape ].remove()

    if touch_stage == 'touch_move':
        # Check if there are any shapes within MAX_DIST. Remove them.
        shape = self.physics_interface.space.nearest_point_query_nearest( Vec2d( *touch.pos ), MAX_DIST, COLLTYPE_USERPLAT )
        if shape and shape.collision_type == COLLTYPE_USERPLAT:
            self.physics_interface.smap[ shape ].remove()
            
    if touch_stage == 'touch_up':
        pass
