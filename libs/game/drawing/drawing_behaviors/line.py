from kivy.graphics import Color, Line
from cymunk import Vec2d

def straightline( self, touch, touch_stage ):
    """Do three different things depending on which touch_stage it is."""
    # When drawing a straight line, offset the touch coordinates so it's easier to see the endpoint.
    if touch_stage == 'touch_down':
        self.x_off = 0
        if self.y + touch.y < self.y + (self.height/2.):
            self.y_off = -100
        else:
            self.y_off = 100

        # Store the initial point of the touch.
        self.line_point1 = Vec2d( touch.x, touch.y )
        self.line_progress = None
        
    if touch_stage == 'touch_move':
        if self.y_off < 0:
            if self.y + touch.y > self.y + (.75*self.height):
                self.y_off = 100
        else:
            if self.y + touch.y < self.y + (.25*self.height):
                self.y_off = -100
        touch.pos = touch.x + self.x_off, touch.y + self.y_off
        touch.x, touch.y = touch.pos

        # Draw a line connecting the initial touch position and the current touch position.
        if self.line_point1:
            if self.line_progress:
                self.canvas.remove( self.line_progress )
            x, y = self.line_point1
            with self.canvas:
                Color( 0,1,0,1)
                self.line_progress = Line( points=[ x,y,touch.x,touch.y ] )

    if touch_stage == 'touch_up':
        self.x_off, self.y_off = 0, 0  

        # Create a physics body that corresponds to a line segment with touch_origin and touch_destination as endpoints.
        if self.line_point1:
            self.line_point1 = None
            
        if self.line_progress:
            lp1 = self.line_progress.points[:2]
            lp2 = self.line_progress.points[2:4]
            self.physics_world.add_user_static_line( lp1, lp2 )

            self.canvas.remove( self.line_progress )
            self.line_progress = None

