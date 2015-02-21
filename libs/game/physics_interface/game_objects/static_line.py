from _env import *

class StaticLine():
    def __init__( self, physics_interface, (x1,y1), (x2,y2), colltype, smap=None ):
        # 1) Create the physics object.
        seg = cy.Segment(physics_interface.space.static_body, Vec2d(x1,y1), Vec2d(x2,y2), 0.0)
        #seg.friction = 0.99
        seg.elasticity = 0.7
        seg.collision_type = colltype
        self.body = seg
        physics_interface.space.add( seg )

        # 2) Create the renderable object.
        with physics_interface.canvas:
            color = Color(0, 1, 0, 1)
            line  = Line( points=[ x1,y1,x2,y2 ] )
            
        self.render_obj = color, line
        self.physics_interface = physics_interface

        # Since queries and collision arbiters generally deal in shapes, it's useful
        # to be able to find the game object from the shape.
        if smap != None:
            smap[ seg ] = self
            self.smap = smap

    def update( self ):
        pass # Nothing changes. This is a static line.
        
    def remove( self ):
        self.physics_interface.space.remove( self.body )
        
        color, line = self.render_obj
        self.physics_interface.canvas.remove( color )
        self.physics_interface.canvas.remove( line )

        del self.smap[ self.body ]

        
