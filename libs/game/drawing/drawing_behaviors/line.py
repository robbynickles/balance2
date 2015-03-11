from kivy.graphics import Color, Line
from cymunk import Vec2d

from utils import distance
from offsets import build_offsets, destroy_offsets, offset_pos
import magnet

def straightline( self, touch, touch_stage, tilt ):
    """Do three different things depending on which touch_stage it is."""

    if touch_stage == 'touch_down':
        # Offset the touch positions to be more visible.
        build_offsets( self, touch.pos )

        # Store the initial point of the touch.
        self.line_point1 = Vec2d( *touch.pos )

        # If the touch is close enough to another user_drawn platform's endpoint, connect them.
        self.line_point1 = magnet.connect( self, self.line_point1 )

        self.line_progress = None
        
    if touch_stage == 'touch_move':

        # Draw a line connecting the initial touch position and the current touch position.
        if self.line_point1:
            if self.line_progress:
                self.canvas.remove( self.line_progress )
            x, y = self.line_point1

            # Offset the touch positions to be more visible.
            touch.pos = offset_pos( self, touch.pos, tilt )
            touch.pos = magnet.connect( self, touch.pos )
            touch.x, touch.y = touch.pos

            with self.canvas:
                Color( 0,1,0,1)
                self.line_progress = Line( points=[ x,y,touch.x,touch.y ], width=3. )

    if touch_stage == 'touch_up':
        destroy_offsets( self )

        # Create a physics body that corresponds to a line segment with touch_origin and touch_destination as endpoints.
        if self.line_point1:
            self.line_point1 = None
            
        if self.line_progress:
            lp1 = self.line_progress.points[:2]
            lp2 = self.line_progress.points[2:4]
            self.physics_interface.add_user_static_line( lp1, lp2 )

            self.canvas.remove( self.line_progress )
            self.line_progress = None


def editline( self, touch, touch_stage, tilt ):
    """Do three different things depending on which touch_stage it is."""

    # editline has access to self.target_line, which is the user_drawn line that triggered the 'edit line' mode activation.
    if touch_stage == 'touch_down':

        # Offset the touch positions to be more visible.
        build_offsets( self, touch.pos )

        # Store the starting endpoints.
        self.line_start = self.target_line.points[:2]
        self.line_end   = self.target_line.points[2:]

        # Booleans used across function calls to know if either endpoint should be moved.
        self.move_start, self.move_end = False, False

        # Move an endpoint if the touch is close enough to it.
        MAX_DIST = 40
        if distance( self.line_start, touch.pos ) <= MAX_DIST:
            self.move_start = True
        if distance( self.line_end, touch.pos ) <= MAX_DIST:
            self.move_end = True

    if touch_stage == 'touch_move':

        if self.move_start or self.move_end:
            # Offset the touch positions to be more visible.
            touch.pos = offset_pos( self, touch.pos, tilt )
            touch.pos = magnet.connect( self, touch.pos )
            touch.x, touch.y = touch.pos

            # Remove the existing user platform entirely.
            self.target_line.remove()

            # Move the starting endpoint to the touch position.
            if self.move_start:
                self.target_line.store_relative( self.physics_interface.pos, 
                                                 self.physics_interface.size, 
                                                 touch.pos,
                                                 self.line_end )

            # Move the ending endpoint to the touch position.
            if self.move_end:
                self.target_line.store_relative( self.physics_interface.pos, 
                                                 self.physics_interface.size, 
                                                 self.line_start,
                                                 touch.pos )
            # Load the updated user platform.
            self.target_line.load_into_physics_interface( self.physics_interface )

            # Update the endpoint circles to match the new orientation.
            self.target_line.draw_endpoints()

    if touch_stage == 'touch_up':
        destroy_offsets( self )
        self.move_start, self.move_end = False, False
        self.line_start, self.line_end = None, None
