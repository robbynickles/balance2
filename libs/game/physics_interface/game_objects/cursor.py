from _env import *

class Cursor():
    def __init__( self, physics_interface, (x, y) ):
        # Add a circle body to the physics engine.
        body = cy.Body(100, 1e9)
        body.position = x, y
        circle = cy.Circle(body, 10)
        #circle.friction = 1.0
        circle.collision_type = COLLTYPE_CURSOR
        physics_interface.space.add(body, circle)
        

        self.physics_interface = physics_interface
        self.body, self.shape = body, circle

    def update( self ):
        pass

    def remove( self ):
        self.physics_interface.space.remove( self.body )
        self.physics_interface.space.remove( self.shape )
