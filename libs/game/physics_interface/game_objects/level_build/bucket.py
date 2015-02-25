from _env import *
from math import sin, cos, pi

class Bucket( GameObject ):
    def set_pos( self, (x,y), (ox,oy), (xdim, ydim) ):
        # Store the points (in percentages, not absolute postions) and color for later use.
        self.relative_pos = (x-ox)/xdim, (y-oy)/ydim
        self.color  = 0,0,1,1

    def rotate( self ):
        # rotate self.angle by 90 degrees
        self.angle = int( ( self.angle + 90 ) % 360 )
    
    def __init__( self, physics_interface, (x, y) ):
        GameObject.__init__( self )

        self.set_pos( (x,y), physics_interface.pos, physics_interface.size )

        # Angle of rotation.
        self.angle = 0

    def rotate_line( self, line, degrees ):
        theta = degrees * (pi/180.)
        rotated_line = []
        ox, oy = self.pos
        for i in range(0, len(line), 2):
            x,y = line[i]-ox, line[i+1]-oy
            rotated_line += [ (x*cos(theta) - y*sin(theta))+ox, (x*sin(theta) + y*cos(theta))+oy ]
        return rotated_line

    def adjust_coordinates( self, (ox,oy), (xdim,ydim) ):
        x, y       = self.relative_pos

        # Find absolute postion based on the passed-in origin and dimensions.
        x, y       = x*xdim+ox, y*ydim+oy
        self.pos   = x, y
        rise, run  = 80, 25

        # Rotate the bucket based on the current value of self.angle.
        self.line1 = self.rotate_line( [x,y,x+run,y+rise], self.angle )
        self.line2 = self.rotate_line( [x,y,x-run,y+rise], self.angle )
        self.line3 = self.rotate_line( [x+(run*.5),y+(rise*.5),x-(run*.5),y+(rise*.5)], self.angle )

    def build_segment( self, space, line ):
        start = line[:2]
        end   = line[2:]
        seg = cy.Segment(space.static_body, Vec2d( start ), Vec2d( end ), 0.0)
        seg.elasticity = 0.7
        return seg

    def build_phys_obj( self, space ):
        seg1 = self.build_segment( space, self.line1 )
        seg2 = self.build_segment( space, self.line2 )
        seg3 = self.build_segment( space, self.line3 )

        # seg3 is the win trigger. When the ball hits it, the level is complete.
        seg3.collision_type = COLLTYPE_BUCKET
        seg3.elasticity = -0.5 # Keep the ball from bouncing out.

        def ball_hit_bucket(space, arbiter): 
            self.physics_interface.add_notification( self, 'Level Complete' )

        submit_collision_handler( COLLTYPE_BUCKET, COLLTYPE_BALL, ball_hit_bucket )

        self.shapes += [ seg1, seg2, seg3 ]

    def build_render_obj( self ):
        color = Color( *self.color )
        line1  = Line( points=self.line1 )
        line2  = Line( points=self.line2 )
        line3  = Line( points=self.line3 )

        self.render_obj = color, line1, line2, line3
        return self.render_obj

