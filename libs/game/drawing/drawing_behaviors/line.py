from kivy.graphics import Color, Line
from cymunk import Vec2d

from utils import distance
from offsets import build_offsets, destroy_offsets, offset_pos
import magnet

def drawline( self, touch, touch_stage, magnetize, curve=False ):
    """Do three different things depending on which touch_stage it is."""

    if touch_stage == 'touch_down':
        # Offset the touch positions to be more visible.
        build_offsets( self, touch.pos )

        # Store the initial point of the touch.
        self.line_point1 = Vec2d( *touch.pos )

        # If the touch is close enough to another user_drawn platform's endpoint, connect them.
        if magnetize:
            self.line_point1 = magnet.connect( self, self.line_point1 )

        self.line_progress = None
        
    if touch_stage == 'touch_move':

        # Draw a line connecting the initial touch position and the current touch position.
        if self.line_point1:
            if self.line_progress:
                self.canvas.remove( self.line_progress )


            # Offset the touch positions to be more visible.
            touch.pos = offset_pos( self, touch.pos )
            if magnetize:
                touch.pos = magnet.connect( self, touch.pos )

            touch.x, touch.y = touch.pos #update touch.x and touch.y
            x, y = self.line_point1

            if curve:
                color = ( 1,0,1,1)
            else:
                color = ( 0,1,0,1)

            with self.canvas:
                Color( *color )
                self.line_progress = Line( points=[ x,y,touch.x,touch.y ], width=3. )

    if touch_stage == 'touch_up':
        destroy_offsets( self )

        # Create a physics body that corresponds to a line segment with touch_origin and touch_destination as endpoints.
        if self.line_point1:
            self.line_point1 = None
            
        if self.line_progress:
            lp1 = self.line_progress.points[:2]
            lp2 = self.line_progress.points[2:4]

            # Don't draw anything if the touch is a quick and short tap.
            if not self.quick_and_short( touch ):
                if curve:
                    self.physics_interface.add_user_static_curve( lp1, lp2 )
                else:
                    self.physics_interface.add_user_static_line( lp1, lp2 )


            self.canvas.remove( self.line_progress )
            self.line_progress = None


def editline( self, touch, touch_stage, magnetize ):
    """Do three different things depending on which touch_stage it is."""

    # editline has access to self.target_line, which is the user_drawn line that triggered the 'edit line' mode activation.
    if touch_stage == 'touch_down':

        # Offset the touch positions to be more visible.
        build_offsets( self, touch.pos, offset=0 )

        # Booleans used across function calls to know if either endpoint should be moved.
        self.move_start, self.move_end = False, False

        # Move an endpoint if the touch is close enough to it.
        if self.target_line.near_start( touch.pos ):
            self.move_start = True
        if self.target_line.near_end( touch.pos ):
            self.move_end = True

    if touch_stage == 'touch_move':

        SIGNIFICANT = 20
        # If the magnitude of the displacement since the last touch is significant, 
        # offset the touch positions to be more visible.
        if distance( (0,0), touch.dpos ) >= SIGNIFICANT:
            build_offsets( self, touch.pos, offset=200 )

        try:
            # Offset the touch positions to be more visible.
            touch.pos = offset_pos( self, touch.pos )
        except: # The offsets weren't setup. Don't do anything more.
            return

        if magnetize:
            touch.pos = magnet.connect( self, touch.pos )
            
        origin, dim = self.physics_interface.pos, self.physics_interface.size
        
        # Move the starting endpoint to the touch position.
        if self.move_start:
            self.target_line.set_start( origin, dim, touch.pos )

        # Move the ending endpoint to the touch position.
        elif self.move_end:
            self.target_line.set_end( origin, dim, touch.pos )
            
        # Move the middle point to the touch position.
        elif self.target_line.curve:
            self.target_line.set_thirdpt( origin, dim, touch.pos )

        # Update the render_obj to match the current orientation.
        self.target_line.adjust_coordinates(origin, dim)
        self.target_line.update_render_obj()
        self.target_line.update_endpoints()

    if touch_stage == 'touch_up':
        destroy_offsets( self )
        self.move_start, self.move_end = False, False
        self.line_start, self.line_end = None, None
        self.exit_edit_line_mode()
