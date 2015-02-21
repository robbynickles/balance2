from _env import *

class PreStaticLine(GameObject):
    def __init__( self, world, (x1,y1), (x2,y2), smap=None ):
        # Store the points (in percentages, not absolute postions) and color for later use.
        ox, oy      = world.pos
        xdim, ydim  = world.size
        self.relative_points = (x1-ox)/xdim, (y1-oy)/ydim, (x2-ox)/xdim, (y2-oy)/ydim
        self.color  = 1,0,0,1

        self.smap = smap

        # Represent the object on the level-builder screen.
        self.load_into_space_and_context( world.space, 
                                          world.canvas,
                                          world.pos, 
                                          world.size )

    def adjust_coordinates( self, pos, size ):
        ox, oy         = pos
        xdim, ydim     = size
        x1, y1, x2, y2 = self.relative_points

        # Find absolute postion based on the passed-in pos and size.
        x1, y1, x2, y2 = x1*xdim+ox, y1*ydim+oy, x2*xdim+ox, y2*ydim+oy
        self.points = x1, y1, x2, y2

    ##### Delayed execution of body building and canvas instruction building:
    def build_phys_obj( self, space ):
        x1, y1, x2, y2 = self.points
        seg = cy.Segment(space.static_body, Vec2d(x1,y1), Vec2d(x2,y2), 0.0)
        #seg.friction = 0.99
        seg.elasticity = 0.7
        seg.collision_type = COLLTYPE_LAVA

        def ball_hit_lava(space, arbiter): 
            # Remove the ball.
            # Flash the screen red.
            # Reset the gamelayout.
            pass

        submit_collision_handler( COLLTYPE_LAVA, COLLTYPE_BALL, ball_hit_lava )

        self.body = seg
        if self.smap != None:
            self.smap[ self.body ] = self

    def build_render_obj( self, context ):
        color = Color( *self.color )
        line  = Line( points=self.points )
        self.render_obj = color, line
    
