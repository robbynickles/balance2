from kivy.graphics import Color, Line, Bezier
from cymunk import Vec2d

import cymunk as cy

#from scipy import signal
#import numpy as np


def freehand( self, touch, touch_stage ):
    """Do three different things depending on which touch_stage it is."""

    if touch_stage == 'touch_down':
        # Store the initial point of the touch.
        self.line_points = [ touch.x, touch.y ]
        self.line_progress = None
        
    if touch_stage == 'touch_move':
        # Draw a line connecting all touch points.
        self.line_points += [ touch.x, touch.y ]
        if self.line_progress:
            self.canvas.remove( self.line_progress )
        with self.canvas:
            Color( 0,1,0,1)
            #self.line_progress = Bezier( points=self.line_points )
            self.line_progress = Line( points=self.line_points )

    if touch_stage == 'touch_up':
        # Remove the line drawing.
        if self.line_progress:
            self.canvas.remove( self.line_progress )

        self.line_points += [ touch.x, touch.y ]

        # Attempt at low-pass filtering the noisy user-drawn curve.
        #X, Y = [], []
        #for i in range( 0, len( self.line_points ), 2 ):
        #    X += [ self.line_points[i] ]
        #    Y += [ self.line_points[i+1] ]

        #array           = np.array( Y, np.float32 )
        #filtered_points = signal.wiener(array)
        #new_points      = []
        #for x, y in zip( X, filtered_points ):
        #    new_points += [ x, y ]
     
        # Create a physics world freehand line.
        #self.physics_interface.add_user_freehand_line( new_points )
        self.physics_interface.add_user_freehand_line( self.line_points )

        self.line_points = []
